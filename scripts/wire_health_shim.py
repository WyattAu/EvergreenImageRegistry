#!/usr/bin/env python3
"""
wire_health_shim.py — Wire health-shim into all EvergreenImageRegistry Dockerfiles.

Reads .shim-version for the version tag. Handles scratch, wolfi, and distroless base images.
Adds ARG SHIM_VERSION for repo-wide version management.

Usage:
    python3 scripts/wire_health_shim.py [--dry-run] [--force] [--image NAME]
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
VERSION_FILE = REPO_ROOT / ".shim-version"

# Images to skip (CLI tools, no service, already handled specially)
SKIP_IMAGES = {
    "health-shim",  # IS the shim
    "forgejo-runner-k8s",  # No HEALTHCHECK
    "scratch-base",  # Reference image
    "distroless",  # Reference image
    "distroless-cassandra",  # Reference image
    "_wip",  # WIP directory
    "_archive",  # Archived
}

# CLI-only images (no EXPOSE, no service port)
CLI_ONLY = {
    "cosign",
    "step-cli",
    "age",
    "crane",
    "helm",
    "kubectl",
    "buildx",
    "scratch-go",
    "restic",
    "rclone",
    "syft",
    "grype",
    "trivy",
    "sops",
    "jq",
    "yq",
    "kubeseal",
    "flux",
}


def read_shim_version() -> str:
    """Read the shim version from .shim-version file."""
    if not VERSION_FILE.exists():
        print(f"WARNING: {VERSION_FILE} not found, using v0.2.0", file=sys.stderr)
        return "v0.2.0"
    version = VERSION_FILE.read_text().strip()
    if not version:
        return "v0.2.0"
    return version


def detect_base_type(content: str) -> str:
    """Detect the base image type of the final stage."""
    lines = content.split("\n")
    for line in reversed(lines):
        stripped = line.strip()
        if stripped.upper().startswith("FROM "):
            lower = stripped.lower()
            if "scratch" in lower:
                return "scratch"
            elif "wolfi" in lower:
                return "wolfi"
            elif "distroless" in lower:
                return "distroless"
            elif "debian" in lower or "ubuntu" in lower:
                return "debian"
            elif "alpine" in lower:
                return "alpine"
            else:
                return "other"
    return "unknown"


def detect_health_port(content: str) -> int | None:
    """Extract the health check port from the Dockerfile."""
    lines = content.split("\n")

    # 1. From existing HEALTHCHECK wget/curl URL
    for line in lines:
        if "HEALTHCHECK" in line.upper() and "NONE" not in line.upper():
            match = re.search(r"localhost:(\d+)", line)
            if match:
                port = int(match.group(1))
                if port != 9101:  # Skip shim's own metrics port
                    return port

    # 2. From EXPOSE directive (first non-9101 port)
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("EXPOSE "):
            ports = re.findall(r"(\d+)", stripped.split(None, 1)[1])
            for p in ports:
                port = int(p)
                if port != 9101:
                    return port

    return None


def detect_entrypoint(content: str) -> str | None:
    """Extract the current entrypoint binary path."""
    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("ENTRYPOINT "):
            # JSON array form: ENTRYPOINT ["/binary"] or ENTRYPOINT ["/binary", "arg"]
            match = re.search(r'\["([^"]+)"', stripped)
            if match:
                return match.group(1)
            # Shell form: ENTRYPOINT /binary
            match = re.search(r"ENTRYPOINT\s+(\S+)", stripped)
            if match:
                return match.group(1)
    return None


def detect_entrypoint_args(content: str) -> list:
    """Extract the full ENTRYPOINT as a list of args."""
    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("ENTRYPOINT "):
            # JSON array form
            match = re.search(r"\[(.+)\]", stripped)
            if match:
                try:
                    import json

                    return json.loads("[" + match.group(1) + "]")
                except (json.JSONDecodeError, IndexError):
                    pass
            # Shell form - return as single element
            match = re.search(r"ENTRYPOINT\s+(.+)", stripped)
            if match:
                return [match.group(1)]
    return []


def detect_cmd(content: str) -> str | None:
    """Extract the current CMD as a string."""
    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("CMD "):
            return stripped[4:].strip()
    return None


def detect_cmd_args(content: str) -> list:
    """Extract CMD as a list of args."""
    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("CMD "):
            # JSON array form
            match = re.search(r"\[(.+)\]", stripped)
            if match:
                try:
                    import json

                    return json.loads("[" + match.group(1) + "]")
                except (json.JSONDecodeError, IndexError):
                    pass
            # Shell form
            return [stripped[4:].strip()]
    return []


def has_shim_stage(content: str) -> bool:
    """Check if the Dockerfile already has a shim stage."""
    return "evergreenshim/health-shim" in content.lower()


def has_shim_wiring(content: str) -> bool:
    """Check if the Dockerfile already has shim COPY/ENTRYPOINT."""
    return "COPY --from=shim" in content and (
        "/shim" in content or "/usr/local/bin/shim" in content
    )


def detect_healthcheck_type(content: str) -> str:
    """Detect whether existing healthcheck uses HTTP or TCP."""
    lines = content.split("\n")
    for line in lines:
        if "HEALTHCHECK" in line.upper() and "NONE" not in line.upper():
            if "wget" in line.lower() or "curl" in line.lower():
                return "http"
            if "pg_isready" in line or "mysqladmin" in line or "mariadb-admin" in line:
                return "exec"
    return "tcp"


def extract_http_healthcheck_path(content: str) -> str | None:
    """Extract the path from an HTTP healthcheck (e.g., /healthz, /api/healthz)."""
    lines = content.split("\n")
    for line in lines:
        if "HEALTHCHECK" in line.upper() and "NONE" not in line.upper():
            # wget -qO- http://localhost:PORT/PATH
            match = re.search(r"localhost:\d+(/\S*)", line)
            if match:
                path = match.group(1).rstrip("/").rstrip("'").rstrip('"')
                if path:
                    return path
    return None


def build_wired_dockerfile(
    content: str,
    shim_version: str,
    base_type: str,
    health_port: int,
    entrypoint: str,
    cmd_args: list,
    image_name: str,
) -> str:
    """Build the wired Dockerfile with health-shim integration."""
    lines = content.split("\n")
    result = []

    # 1. Add ARG SHIM_VERSION after the first FROM (or at top if no build stage)
    shim_copy_added = False
    entrypoint_replaced = False
    cmd_replaced = False
    healthcheck_replaced = False
    already_has_shim_stage = has_shim_stage(content)

    # Find the final stage FROM line
    final_from_idx = None
    from_count = 0
    for i, line in enumerate(lines):
        if line.strip().upper().startswith("FROM "):
            from_count += 1
            final_from_idx = i

    # Add ARG before first FROM if not already present
    arg_added = False
    for i, line in enumerate(lines):
        stripped = line.strip()

        # Add ARG SHIM_VERSION before first FROM
        if (
            not arg_added
            and stripped.upper().startswith("FROM ")
            and not already_has_shim_stage
        ):
            if i > 0 and "ARG SHIM_VERSION" in lines[i - 1]:
                arg_added = True  # Already has ARG
            else:
                result.append(f"ARG SHIM_VERSION={shim_version}")
                result.append("")
                arg_added = True

        # Add shim stage before final FROM (if not already present)
        if i == final_from_idx and not already_has_shim_stage:
            shim_ref = "ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION}"
            result.append(f"FROM {shim_ref} AS shim")
            result.append("")

        # After final stage FROM, add COPY --from=shim
        if i == final_from_idx and not shim_copy_added:
            result.append(line)
            shim_copy_added = True

            # Always copy shim to canonical path /usr/local/bin/shim
            # Docker COPY creates parent dirs, so this works for scratch too.
            result.append("COPY --from=shim /shim /usr/local/bin/shim")
            result.append("RUN chmod +x /usr/local/bin/shim || true")

            result.append("")
            continue

        # Skip original HEALTHCHECK line (we'll add our own)
        if stripped.upper().startswith("HEALTHCHECK ") and not healthcheck_replaced:
            healthcheck_replaced = True
            # Don't add the original - we'll add our own later
            continue

        # Replace ENTRYPOINT
        if stripped.upper().startswith("ENTRYPOINT ") and not entrypoint_replaced:
            entrypoint_replaced = True
            result.append('ENTRYPOINT ["/usr/local/bin/shim", "run"]')
            continue

        # Replace CMD
        if stripped.upper().startswith("CMD ") and not cmd_replaced:
            cmd_replaced = True
            # Build new CMD: -c <original_entrypoint> -- <original_args>
            # We need to construct: ["-c", "/path/to/binary", "--", "arg1", "arg2"]
            cmd_parts = ["-c", entrypoint, "--"]
            # Add original CMD args (excluding the JSON wrapper)
            if cmd_args:
                for arg in cmd_args:
                    if arg != entrypoint:  # Don't duplicate the entrypoint
                        cmd_parts.append(arg)
            result.append(f"CMD {json.dumps(cmd_parts)}")
            continue

        result.append(line)

    # If we haven't added shim COPY yet (edge case), add at end
    if not shim_copy_added:
        result.append("COPY --from=shim /shim /usr/local/bin/shim")

    # Add HEALTHCHECK before ENTRYPOINT (or at end)
    healthcheck_line = (
        f"HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \\\n"
        f'  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:{health_port}"]'
    )

    # Insert HEALTHCHECK before ENTRYPOINT
    final_result = []
    inserted_healthcheck = False
    for line in result:
        if line.strip().upper().startswith("ENTRYPOINT ") and not inserted_healthcheck:
            final_result.append(healthcheck_line)
            final_result.append("")
            inserted_healthcheck = True
        final_result.append(line)

    # If no ENTRYPOINT found, add at end
    if not inserted_healthcheck:
        final_result.append("")
        final_result.append(healthcheck_line)

    return "\n".join(final_result)


def process_image(
    image_dir: Path,
    shim_version: str,
    dry_run: bool = False,
    force: bool = False,
) -> tuple:
    """Process a single image directory. Returns (status, message)."""
    dockerfile = image_dir / "Dockerfile"
    if not dockerfile.exists():
        return "skip", "no Dockerfile"

    image_name = image_dir.name
    content = dockerfile.read_text()

    # Skip conditions
    if image_name in SKIP_IMAGES or image_name in CLI_ONLY:
        return "skip", "CLI tool or reference image"

    if has_shim_wiring(content) and not force:
        return "skip", "already wired"

    # Detect properties
    base_type = detect_base_type(content)
    health_port = detect_health_port(content)
    entrypoint = detect_entrypoint(content)

    if not health_port:
        return "skip", "no EXPOSE port detected"

    if not entrypoint:
        return "skip", "no ENTRYPOINT detected"

    # Skip images with no service (UDP-only, sleep, etc.)
    entrypoint_lower = entrypoint.lower()
    if entrypoint_lower in ("sleep", "/bin/sh", "/bin/bash", "sh", "bash"):
        return "skip", f"non-service entrypoint: {entrypoint}"

    cmd_args = detect_cmd_args(content)

    # Build wired version
    try:
        wired = build_wired_dockerfile(
            content,
            shim_version,
            base_type,
            health_port,
            entrypoint,
            cmd_args,
            image_name,
        )
    except Exception as e:
        return "error", f"build failed: {e}"

    if dry_run:
        return (
            "would-wire",
            f"base={base_type}, port={health_port}, entrypoint={entrypoint}",
        )

    # Write the wired Dockerfile
    dockerfile.write_text(wired)
    return "wired", f"base={base_type}, port={health_port}, entrypoint={entrypoint}"


def main():
    parser = argparse.ArgumentParser(
        description="Wire health-shim into EvergreenImageRegistry images"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Don't write files, just report"
    )
    parser.add_argument(
        "--force", action="store_true", help="Re-wire already wired images"
    )
    parser.add_argument("--image", type=str, help="Process only this image")
    args = parser.parse_args()

    shim_version = read_shim_version()
    print(f"Shim version: {shim_version}")
    print(f"Images directory: {IMAGES_DIR}")
    print()

    if not IMAGES_DIR.exists():
        print(f"ERROR: {IMAGES_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    # Collect image dirs
    image_dirs = sorted(
        [d for d in IMAGES_DIR.iterdir() if d.is_dir() and not d.name.startswith("_")]
    )

    if args.image:
        image_dirs = [d for d in image_dirs if d.name == args.image]
        if not image_dirs:
            print(f"ERROR: Image '{args.image}' not found", file=sys.stderr)
            sys.exit(1)

    # Process each image
    stats = {"wired": 0, "skip": 0, "error": 0, "would-wire": 0}
    errors = []

    for image_dir in image_dirs:
        status, msg = process_image(image_dir, shim_version, args.dry_run, args.force)
        stats[status] = stats.get(status, 0) + 1

        if status == "error":
            errors.append(f"  {image_dir.name}: {msg}")
            print(f"  ERROR  {image_dir.name}: {msg}")
        elif status == "wired":
            print(f"  WIRE   {image_dir.name}: {msg}")
        elif status == "would-wire":
            print(f"  WOULD  {image_dir.name}: {msg}")
        elif (
            status == "skip"
            and msg != "CLI tool or reference image"
            and msg != "already wired"
        ):
            print(f"  SKIP   {image_dir.name}: {msg}")

    print()
    print(
        f"Summary: {stats.get('wired', 0)} wired, {stats.get('would-wire', 0)} would-wire, "
        f"{stats.get('skip', 0)} skipped, {stats.get('error', 0)} errors"
    )

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(e)

    if args.dry_run:
        print("\n[DRY RUN] No files were modified")


if __name__ == "__main__":
    main()
