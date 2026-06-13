#!/usr/bin/env python3
"""
integrate_checksum_verification.py - Add sha256sum verification to Dockerfiles.

Reads each CHECKSUMS file for the verified SHA256 hash, then modifies the
corresponding Dockerfile to insert a checksum verification step after the
curl download command.

Usage:
  python3 scripts/integrate_checksum_verification.py [--dry-run] [--image <name>]

Exit codes:
  0 - All integrations successful
  1 - Some integrations failed
  2 - Script error
"""

import argparse
import logging
import re
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"


def log(msg: str, level: str = "INFO"):
    if level == "ERROR":
        logger.error(msg)
    elif level == "WARN":
        logger.warning(msg)
    else:
        logger.info(msg)


def parse_checksums(checksums_path: Path) -> dict | None:
    """Parse a CHECKSUMS TOML file and extract the expected SHA256 hash."""
    content = checksums_path.read_text()

    # Skip non-verified files
    if 'expected_sha256 = "PENDING"' in content or 'expected_sha256 = "N/A"' in content:
        return None

    # Extract expected_sha256
    match = re.search(r'expected_sha256\s*=\s*"([0-9a-fA-F]{64})"', content)
    if not match:
        return None

    sha256 = match.group(1).lower()

    # Extract verification method
    method = "unknown"
    method_match = re.search(r'verification_method\s*=\s*"([^"]+)"', content)
    if method_match:
        method = method_match.group(1)

    # Extract download URL
    url = ""
    url_match = re.search(r'url\s*=\s*"([^"]+)"', content)
    if url_match:
        url = url_match.group(1)

    return {"sha256": sha256, "method": method, "url": url}


def find_curl_download_line(content: str) -> tuple[int, str, str] | None:
    """Find the curl download line in a Dockerfile.

    Returns (line_number, line_content, download_url) or None.
    """
    lines = content.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue

        # Look for curl download patterns
        match = re.search(r'curl\s+-[^\s]*\s+"([^"]+)"\s+-o', line)
        if not match:
            match = re.search(r"curl\s+-[^\s]*\s+'([^']+)'\s+-o", line)

        if match:
            url = match.group(1)
            if not url or url == '""':
                continue
            if url.startswith("http://localhost") or url.startswith("http://127."):
                continue
            return (i, line, url)

    return None


def integrate_checksum_into_dockerfile(
    dockerfile_path: Path, sha256: str, dry_run: bool = False
) -> bool:
    """Insert sha256sum verification into a Dockerfile after the curl download.

    Returns True if successful, False otherwise.
    """
    content = dockerfile_path.read_text()

    result = find_curl_download_line(content)
    if result is None:
        return False

    line_num, line, url = result
    lines = content.splitlines()

    # Find the output filename from curl -o <file>
    output_match = re.search(r"-o\s+/(\S+)", line)
    if not output_match:
        return False

    output_file = output_match.group(1).rstrip("\\").rstrip()
    # Remove trailing backslash continuation
    output_file = output_file.rstrip("\\")

    # Check if this Dockerfile already has sha256sum verification
    for check_line in lines:
        if "sha256sum" in check_line and sha256[:16] in check_line:
            return True  # Already integrated

    # Find the line that contains the curl download command
    # We need to find the RUN line that starts the curl command
    run_line_num = line_num
    while run_line_num >= 0 and "RUN" not in lines[run_line_num]:
        run_line_num -= 1

    if run_line_num < 0:
        return False

    # Determine the indentation
    run_line = lines[run_line_num]
    indent_match = re.match(r"^(\s*)RUN", run_line)
    indent = indent_match.group(1) if indent_match else "    "

    # Build the verification line
    # Pattern: echo "<sha256>  <output_file>" | sha256sum -c -
    verify_line = f'{indent}    echo "{sha256}  /{output_file}" | sha256sum -c - && \\'

    # Insert after the curl download line (before tar extraction)
    # The typical pattern is:
    #   RUN curl -fsSL "URL" -o /file.tar.gz && \
    #       tar -xzf /file.tar.gz ...
    # We insert between curl and tar:
    #   RUN curl -fsSL "URL" -o /file.tar.gz && \
    #       echo "hash  /file.tar.gz" | sha256sum -c - && \
    #       tar -xzf /file.tar.gz ...

    # Find the curl download line in the RUN block
    # It's the line that contains the curl command
    insert_after = line_num

    # Check if the curl line ends with a continuation
    if line.rstrip().endswith("\\"):
        # Insert after this line, before the next command
        lines.insert(insert_after + 1, verify_line)
    else:
        # The curl is the last command on its line, add verification
        lines[insert_after] = line.rstrip() + " && \\"
        lines.insert(insert_after + 1, verify_line)

    # Fix the next line's continuation if needed
    # The verify_line ends with \, so the next line should continue normally
    # But we need to make sure the original continuation still works

    new_content = "\n".join(lines) + "\n"

    if dry_run:
        return True

    dockerfile_path.write_text(new_content)
    return True


def process_image(image_dir: Path, dry_run: bool = False) -> tuple[bool, str]:
    """Process a single image directory.

    Returns (success, status_message) tuple.
    """
    image_name = image_dir.name
    dockerfile_path = image_dir / "Dockerfile"
    checksums_path = image_dir / "CHECKSUMS"

    if not dockerfile_path.exists():
        return True, "No Dockerfile"

    if not checksums_path.exists():
        return True, "No CHECKSUMS"

    # Parse checksums
    checksum_data = parse_checksums(checksums_path)
    if checksum_data is None:
        return True, "Not verified (PENDING/N/A)"

    sha256 = checksum_data["sha256"]
    method = checksum_data["method"]

    # Check if already integrated
    content = dockerfile_path.read_text()
    if "sha256sum" in content:
        return True, "Already has sha256sum"

    if dry_run:
        log(
            f"{image_name}: Would add sha256sum verification (method: {method})", "INFO"
        )
        return True, "dry-run"

    # Integrate
    success = integrate_checksum_into_dockerfile(dockerfile_path, sha256, dry_run=False)
    if success:
        log(f"{image_name}: Added sha256sum verification", "INFO")
        return True, "integrated"
    else:
        log(f"{image_name}: FAILED to integrate checksum verification", "ERROR")
        return False, "integration failed"


def main():

    parser = argparse.ArgumentParser(
        description="Add sha256sum verification to Dockerfiles"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without writing"
    )
    parser.add_argument("--image", type=str, help="Process only this image name")
    args = parser.parse_args()

    if args.dry_run:
        log("DRY RUN MODE - no files will be modified", "WARN")

    if args.image:
        image_dirs = [IMAGES_DIR / args.image]
        if not image_dirs[0].is_dir():
            logger.error(f"Image directory not found: {image_dirs[0]}")
            sys.exit(2)
    else:
        image_dirs = sorted([d for d in IMAGES_DIR.iterdir() if d.is_dir()])

    success_count = 0
    fail_count = 0
    skip_count = 0
    integrated_count = 0

    for image_dir in image_dirs:
        success, status = process_image(image_dir, dry_run=args.dry_run)
        if success:
            if status in ("integrated", "dry-run"):
                integrated_count += 1
            else:
                skip_count += 1
            success_count += 1
        else:
            fail_count += 1

    print()
    print("=" * 60)
    print(
        f"Results: {integrated_count} integrated, {fail_count} failed, {skip_count} skipped"
    )
    print("=" * 60)

    if fail_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
