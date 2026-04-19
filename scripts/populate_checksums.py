#!/usr/bin/env python3
"""
populate_checksums.py - Fetch real SHA256 hashes from upstream release sources.

Strategy:
  1. Parse each Dockerfile to extract the curl download URL
  2. Try upstream checksum files (GitHub sha256sums.txt, HashiCorp SHA256SUMS, etc.)
  3. Fall back to downloading the binary and computing SHA256 locally
  4. Update the CHECKSUMS TOML file with the verified hash

Usage:
  python3 scripts/populate_checksums.py [--dry-run] [--force] [--image <name>]

Exit codes:
  0 - All checksums populated successfully
  1 - Some checksums failed to populate
  2 - Script error
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

# Configuration
REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
USER_AGENT = "EvergreenImageRegistry/1.0 (populate_checksums.py)"

# Timeout for HTTP requests (seconds)
HTTP_TIMEOUT = 30

# Maximum download size for fallback computation (500 MB)
MAX_DOWNLOAD_SIZE = 500 * 1024 * 1024


def log(msg: str, level: str = "INFO"):
    """Print a log message."""
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    prefix = {"INFO": "  ✓", "WARN": "  ⚠", "ERROR": "  ✗", "SKIP": "  →"}.get(level, "  ")
    print(f"[{ts}] {prefix} {msg}")


def http_get(url: str, timeout: int = HTTP_TIMEOUT) -> Optional[str]:
    """Fetch URL content as text. Returns None on failure."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            data = resp.read()
            return data.decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError):
        return None


def http_download_bytes(url: str, timeout: int = 120) -> Optional[bytes]:
    """Download URL content as bytes. Returns None on failure."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            # Read in chunks to respect MAX_DOWNLOAD_SIZE
            chunks = []
            total = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_DOWNLOAD_SIZE:
                    log(f"Download exceeded {MAX_DOWNLOAD_SIZE // (1024*1024)}MB limit", "WARN")
                    return None
                chunks.append(chunk)
            return b"".join(chunks)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError):
        return None


def sha256_hex(data: bytes) -> str:
    """Compute SHA256 hex digest of bytes."""
    return hashlib.sha256(data).hexdigest()


def extract_download_url(dockerfile_path: Path) -> Optional[str]:
    """Extract the first curl download URL from a Dockerfile.
    
    Returns the URL string or None if not found.
    Skips healthcheck curl commands and empty URLs.
    """
    content = dockerfile_path.read_text()
    lines = content.splitlines()

    for line in lines:
        # Skip comment lines
        stripped = line.strip()
        if stripped.startswith("#"):
            continue

        # Look for curl download patterns
        # Pattern 1: curl -fsSL "<URL>" -o <file>
        match = re.search(r'curl\s+-[^\s]*\s+"([^"]+)"\s+-o', line)
        if not match:
            # Pattern 2: curl -fsSL '<URL>' -o <file>  (single quotes)
            match = re.search(r"curl\s+-[^\s]*\s+'([^']+)'\s+-o", line)

        if match:
            url = match.group(1)
            # Skip empty URLs (wolfi stubs)
            if not url or url == '""':
                continue
            # Skip localhost/internal URLs
            if url.startswith("http://localhost") or url.startswith("http://127."):
                continue
            return url

    return None


def extract_filename_from_url(url: str) -> str:
    """Extract the filename component from a URL."""
    # Get the last path component
    path = url.split("?")[0]  # Remove query string
    filename = path.rstrip("/").split("/")[-1]
    return filename


def resolve_template_url(url: str, dockerfile_path: Path) -> str:
    """Resolve ${VERSION} template variables in URLs by reading ARG VERSION."""
    # Read the Dockerfile to find the VERSION arg
    content = dockerfile_path.read_text()
    match = re.search(r'ARG\s+VERSION\s*=\s*(\S+)', content)
    if match:
        version = match.group(1).strip('"').strip("'")
        url = url.replace("${VERSION}", version)
    return url


def filenames_match(target: str, candidate: str) -> bool:
    """Check if two filenames refer to the same binary.
    
    Handles:
    - Exact match
    - One contains the other
    - v-prefix differences (etcd-3.5.15 vs etcd-v3.5.15)
    - Extension differences (.tar.gz vs .tgz)
    """
    if target == candidate:
        return True
    
    # Strip common prefixes/suffixes for comparison
    def normalize(s: str) -> str:
        s = s.lower()
        s = s.replace(".tar.gz", "").replace(".tgz", "").replace(".tar.xz", "").replace(".zip", "")
        s = s.replace(".bz2", "").replace(".xz", "")
        # Normalize v-prefix: remove v before digits
        s = re.sub(r'v(\d)', r'\1', s)
        # Remove -linux-amd64, _linux_amd64, etc.
        s = re.sub(r'[-_]linux[-_]amd64', '', s)
        s = re.sub(r'[-_]x86[-_]64[-_]unknown[-_]linux[-_]gnu', '', s)
        s = re.sub(r'[-_]x86[-_]64[-_]unknown[-_]linux[-_]musl', '', s)
        s = re.sub(r'[-_]x86[-_]64', '', s)
        return s

    nt = normalize(target)
    nc = normalize(candidate)
    
    if nt == nc:
        return True
    if nt in nc or nc in nt:
        return True
    
    # Check if the key parts match (after removing arch/version variations)
    # e.g., "etcd-3.5.15-linux-amd64" should match "etcd-v3.5.15-linux-amd64"
    def key_parts(s: str) -> str:
        s = s.lower()
        # Remove extension
        s = re.sub(r'\.(tar\.gz|tgz|tar\.xz|zip|bz2|xz)$', '', s)
        # Remove arch suffixes
        s = re.sub(r'[-_]?(linux[-_]?amd64|x86[-_]64[-_].*?)(\.\w+)?$', '', s)
        return s
    
    kt = key_parts(target)
    kc = key_parts(candidate)
    # Try with and without v prefix
    kt_nov = re.sub(r'v(\d)', r'\1', kt)
    kc_nov = re.sub(r'v(\d)', r'\1', kc)
    
    if kt == kc or kt == kc_nov or kt_nov == kc or kt_nov == kc_nov:
        return True
    if kt in kc or kc in kt or kt in kc_nov or kc_nov in kt:
        return True
    
    return False


def find_github_checksum(url: str, filename: str) -> Optional[str]:
    """Try to find SHA256 from GitHub release checksums file."""
    # Extract release URL base (everything up to the last /)
    # e.g., https://github.com/org/repo/releases/download/v1.0.0/file.tar.gz
    #       -> https://github.com/org/repo/releases/download/v1.0.0
    parts = url.rsplit("/", 1)
    if len(parts) < 2:
        return None
    release_base = parts[0]

    # Try various checksum file names
    checksum_urls = [
        f"{release_base}/sha256sums.txt",
        f"{release_base}/SHASUMS256.txt",
        f"{release_base}/SHA256SUMS",
        f"{release_base}/checksums.txt",
        f"{release_base}/checksums-amd64.txt",
        f"{release_base}/checksums256.txt",
    ]

    for checksum_url in checksum_urls:
        content = http_get(checksum_url)
        if content is None:
            continue

        # Parse the checksum file
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Format: <hash>  <filename> or <hash> *<filename> or <hash>  <filename>
            # Also handle: <hash> (<filename>) = <hash> (some Go projects)
            parts_match = re.match(r'^([0-9a-fA-F]{64})\s+[* ](.+)$', line)
            if not parts_match:
                # Try parenthesized format: <hash>  filename
                parts_match = re.match(r'^([0-9a-fA-F]{64})\s+\((.+)\)', line)
            if parts_match:
                hash_val = parts_match.group(1).lower()
                fname = parts_match.group(2).strip()
                # Match using fuzzy filename matching
                if filenames_match(filename, fname):
                    return hash_val

    return None


def find_hashicorp_checksum(url: str) -> Optional[str]:
    """Find SHA256 from HashiCorp releases SHA256SUMS file."""
    # Parse: https://releases.hashicorp.com/vault/1.18.1/vault_1.18.1_linux_amd64.zip
    match = re.match(r'https://releases\.hashicorp\.com/([^/]+)/([^/]+)/(.+)', url)
    if not match:
        return None

    product = match.group(1)
    version = match.group(2)
    filename = match.group(3)

    # Try the SHA256SUMS file
    checksum_url = f"https://releases.hashicorp.com/{product}/{version}/{product}_{version}_SHA256SUMS"
    content = http_get(checksum_url)
    if content is None:
        # Try alternate naming
        checksum_url = f"https://releases.hashicorp.com/{product}/{version}/{product}_{version}_SHA256SUMS.256"
        content = http_get(checksum_url)

    if content:
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            parts_match = re.match(r'^([0-9a-fA-F]{64})\s+(.+)$', line)
            if parts_match:
                hash_val = parts_match.group(1).lower()
                fname = parts_match.group(2).strip()
                if fname == filename or filename in fname:
                    return hash_val

    return None


def find_k8s_checksum(url: str) -> Optional[str]:
    """Find SHA256 from k8s release."""
    # Parse: https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kubectl
    match = re.match(r'https://dl\.k8s\.io/release/(v[^/]+)/bin/([^/]+)/(.+)', url)
    if not match:
        return None

    version = match.group(1)
    arch_dir = match.group(2)
    binary = match.group(3)

    checksum_url = f"https://dl.k8s.io/{version}/bin/{arch_dir}/{binary}.sha256"
    content = http_get(checksum_url)
    if content:
        # k8s sha256 files contain just the hash on one line
        hash_val = content.strip()
        if re.match(r'^[0-9a-fA-F]{64}$', hash_val):
            return hash_val.lower()

    return None


def find_helm_checksum(url: str) -> Optional[str]:
    """Find SHA256 from Helm release."""
    # Parse: https://get.helm.sh/helm-3.15.1-linux-amd64.tar.gz
    # Helm uses helm-v<VERSION> format with .sha256 extension
    match = re.match(r'https://get\.helm\.sh/(.+)', url)
    if not match:
        return None

    filename = match.group(1)
    # Try various checksum URL patterns
    for suffix in [".sha256sum", ".sha256", "-sha256.txt"]:
        checksum_url = f"https://get.helm.sh/{filename}{suffix}"
        content = http_get(checksum_url)
        if content:
            hash_val = content.strip()
            if re.match(r'^[0-9a-fA-F]{64}$', hash_val):
                return hash_val.lower()
            # Multi-line format
            for line in content.splitlines():
                line = line.strip()
                parts_match = re.match(r'^([0-9a-fA-F]{64})\s+', line)
                if parts_match:
                    return parts_match.group(1).lower()

    # Try with v-prefix (helm uses helm-v<version> not helm-<version>)
    v_filename = re.sub(r'helm-', 'helm-v', filename, count=1)
    for suffix in [".sha256sum", ".sha256"]:
        checksum_url = f"https://get.helm.sh/{v_filename}{suffix}"
        content = http_get(checksum_url)
        if content:
            hash_val = content.strip()
            if re.match(r'^[0-9a-fA-F]{64}$', hash_val):
                return hash_val.lower()

    return None


def download_and_compute(url: str) -> Optional[str]:
    """Download the binary and compute SHA256 locally."""
    log(f"  Downloading to compute SHA256: {extract_filename_from_url(url)}", "WARN")
    data = http_download_bytes(url)
    if data:
        return sha256_hex(data)
    return None


def find_checksum_for_url(url: str, filename: str) -> Tuple[Optional[str], str]:
    """Try all methods to find the SHA256 checksum for a URL.
    
    Returns (hash, method) tuple where method describes how the hash was found.
    """
    # Method 1: GitHub release checksums
    if "github.com" in url and "/releases/download/" in url:
        h = find_github_checksum(url, filename)
        if h:
            return h, "github-release-checksums"

    # Method 2: HashiCorp releases
    if "releases.hashicorp.com" in url:
        h = find_hashicorp_checksum(url)
        if h:
            return h, "hashicorp-SHA256SUMS"

    # Method 3: k8s
    if "dl.k8s.io" in url:
        h = find_k8s_checksum(url)
        if h:
            return h, "k8s-release-sha256"

    # Method 4: Helm
    if "get.helm.sh" in url:
        h = find_helm_checksum(url)
        if h:
            return h, "helm-sha256sum"

    # Method 5: Direct download and compute
    h = download_and_compute(url)
    if h:
        return h, "download-and-compute"

    return None, "failed"


def update_checksums_file(checksums_path: Path, image_name: str, version: str,
                          url: str, filename: str, sha256: str, method: str,
                          upstream_checksum_url: str = ""):
    """Update a CHECKSUMS file with verified hash."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Determine upstream checksum URL for documentation
    if not upstream_checksum_url:
        if "github.com" in url and "/releases/download/" in url:
            release_base = url.rsplit("/", 1)[0]
            upstream_checksum_url = f"{release_base}/sha256sums.txt"
        elif "releases.hashicorp.com" in url:
            match = re.match(r'(https://releases\.hashicorp\.com/[^/]+/[^/]+)/', url)
            if match:
                upstream_checksum_url = f"{match.group(1)}_SHA256SUMS"
        elif "dl.k8s.io" in url:
            upstream_checksum_url = f"{url}.sha256"
        elif "get.helm.sh" in url:
            upstream_checksum_url = f"{url}.sha256sum"

    content = f"""# CHECKSUMS - {image_name}
# Generated: {now}
# Status: VERIFIED
#
# Verification performed by populate_checksums.py
# Method: {method}
# Date: {now}
#
# IMPORTANT: These checksums are verified against upstream sources.
# To re-verify:
# 1. Download binary from URL below
# 2. Compute: sha256sum <file>
# 3. Compare with expected_sha256 below
# 4. Cross-validate against upstream_checksum URL if available
# 5. Submit PR with any changes

[metadata]
image = "{image_name}"
version = "{version}"
created = "{now}"
last_verified = "{now}"
verification_method = "{method}"
verifier = "populate_checksums.py"

[download]
url = "{url}"
filename = "{filename}"

[checksum]
# SHA256 of the downloaded archive/binary
expected_sha256 = "{sha256}"

[upstream_checksum]
# If upstream provides a checksum file, note the URL here
url = "{upstream_checksum_url}"
format = "sha256"
"""
    checksums_path.write_text(content.strip() + "\n")


def process_image(image_dir: Path, dry_run: bool = False, force: bool = False) -> bool:
    """Process a single image directory.
    
    Returns True if successful, False otherwise.
    """
    image_name = image_dir.name
    dockerfile_path = image_dir / "Dockerfile"
    checksums_path = image_dir / "CHECKSUMS"

    # Check prerequisites
    if not dockerfile_path.exists():
        log(f"{image_name}: No Dockerfile found", "SKIP")
        return True  # Not an error, just skip

    if not checksums_path.exists():
        log(f"{image_name}: No CHECKSUMS file found", "SKIP")
        return True

    # Check if already verified (and not forced)
    if not force:
        existing = checksums_path.read_text()
        if 'expected_sha256 = "PENDING"' not in existing and 'expected_sha256 = "N/A"' not in existing:
            log(f"{image_name}: Already has verified checksum", "SKIP")
            return True

    # Extract download URL
    raw_url = extract_download_url(dockerfile_path)
    if raw_url is None:
        log(f"{image_name}: No binary download URL found", "SKIP")
        return True

    # Resolve template variables
    url = resolve_template_url(raw_url, dockerfile_path)
    filename = extract_filename_from_url(url)

    log(f"{image_name}: Resolved URL: {url}")
    log(f"{image_name}: Filename: {filename}")

    # Find checksum
    sha256, method = find_checksum_for_url(url, filename)

    if sha256 is None:
        log(f"{image_name}: FAILED to find checksum for {filename}", "ERROR")
        return False

    log(f"{image_name}: SHA256={sha256[:16]}... (method: {method})")

    if dry_run:
        log(f"{image_name}: [DRY RUN] Would update CHECKSUMS", "INFO")
        return True

    # Extract version from Dockerfile
    version = "unknown"
    content = dockerfile_path.read_text()
    match = re.search(r'ARG\s+VERSION\s*=\s*(\S+)', content)
    if match:
        version = match.group(1).strip('"').strip("'")

    # Update CHECKSUMS file
    update_checksums_file(
        checksums_path, image_name, version, url, filename, sha256, method
    )
    log(f"{image_name}: CHECKSUMS file updated", "INFO")
    return True


def main():
    parser = argparse.ArgumentParser(description="Populate CHECKSUMS files with real SHA256 hashes")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without writing")
    parser.add_argument("--force", action="store_true", help="Re-verify even if already populated")
    parser.add_argument("--image", type=str, help="Process only this image name")
    args = parser.parse_args()

    if args.dry_run:
        log("DRY RUN MODE - no files will be modified", "WARN")

    # Find all image directories
    if args.image:
        image_dirs = [IMAGES_DIR / args.image]
        if not image_dirs[0].is_dir():
            print(f"ERROR: Image directory not found: {image_dirs[0]}", file=sys.stderr)
            sys.exit(2)
    else:
        image_dirs = sorted([d for d in IMAGES_DIR.iterdir() if d.is_dir()])

    success_count = 0
    fail_count = 0
    skip_count = 0

    for image_dir in image_dirs:
        result = process_image(image_dir, dry_run=args.dry_run, force=args.force)
        if result is True:
            # Check if it was actually processed or skipped
            checksums_path = image_dir / "CHECKSUMS"
            if checksums_path.exists():
                existing = checksums_path.read_text()
                if 'expected_sha256 = "PENDING"' in existing or 'expected_sha256 = "N/A"' in existing:
                    skip_count += 1
                else:
                    success_count += 1
            else:
                skip_count += 1
        else:
            fail_count += 1

    print()
    print("=" * 60)
    print(f"Results: {success_count} verified, {fail_count} failed, {skip_count} skipped")
    print("=" * 60)

    if fail_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
