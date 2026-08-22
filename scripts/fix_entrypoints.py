#!/usr/bin/env python3
"""Fix ENTRYPOINT missing -c flag across all EIR images.

For images with ENTRYPOINT ["shim", "run"] (no -c), reads manifest.toml
to find the correct binary path and injects it.
"""

import re
from pathlib import Path

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"
SHIM_PATHS = ("/usr/local/bin/shim", "/shim")


def parse_manifest_entrypoint(toml_path: Path) -> str | None:
    """Extract entrypoint binary from manifest.toml."""
    if not toml_path.exists():
        return None
    text = toml_path.read_text()
    # Match: entrypoint = ["/binary"] or entrypoint = ["binary"]
    m = re.search(r"entrypoint\s*=\s*\[([^\]]+)\]", text)
    if m:
        # Parse the array elements
        elements = re.findall(r'"([^"]+)"', m.group(1))
        if elements:
            return " ".join(elements)
    # Match: command = "/binary"
    m = re.search(r'command\s*=\s*"([^"]+)"', text)
    if m:
        return m.group(1)
    return None


def parse_dockerfile_entrypoint(dockerfile_path: Path) -> tuple[str | None, list[str]]:
    """Find ENTRYPOINT and return (raw_text, args)."""
    text = dockerfile_path.read_text()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("ENTRYPOINT"):
            content = stripped[len("ENTRYPOINT") :].strip()
            match = re.match(r"\[(.*)\]", content)
            if match:
                args = [
                    a.strip().strip('"').strip("'") for a in match.group(1).split(",")
                ]
                return content, args
            return content, content.split()
    return None, []


def parse_dockerfile_cmd(dockerfile_path: Path) -> tuple[str | None, list[str]]:
    """Find CMD and return (raw_text, args)."""
    text = dockerfile_path.read_text()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("CMD") and not stripped.upper().startswith(
            "CMD-SHELL"
        ):
            content = stripped[len("CMD") :].strip()
            match = re.match(r"\[(.*)\]", content)
            if match:
                args = [
                    a.strip().strip('"').strip("'") for a in match.group(1).split(",")
                ]
                return content, args
            return content, content.split()
    return None, []


def is_repack_exempt(dockerfile_path: Path) -> bool:
    """Check if image has repack-upstream-init exemption."""
    text = dockerfile_path.read_text()
    return "repack-upstream-init" in text


def fix_entrypoint(dockerfile_path: Path, binary: str) -> bool:
    """Replace ENTRYPOINT ["shim", "run"] with ["shim", "run", "-c", binary]."""
    text = dockerfile_path.read_text()

    # Pattern: ENTRYPOINT ["/usr/local/bin/shim", "run"] or ENTRYPOINT ["/shim", "run"]
    # Must NOT already have -c
    for shim_path in SHIM_PATHS:
        old = f'ENTRYPOINT ["{shim_path}", "run"]'
        if old in text and "-c" not in text.split(old)[1][:20]:
            new = f'ENTRYPOINT ["{shim_path}", "run", "-c", "{binary}"]'
            text = text.replace(old, new)
            dockerfile_path.write_text(text)
            return True

    return False


def main():
    fixed = 0
    no_manifest = 0
    already_ok = 0
    errors = []

    for img_dir in sorted(IMAGES_DIR.iterdir()):
        if not img_dir.is_dir() or img_dir.name.startswith("_"):
            continue

        img = img_dir.name
        dockerfile = img_dir / "Dockerfile"
        manifest = img_dir / "manifest.toml"

        if not dockerfile.exists():
            continue

        # Skip repack-exempt images
        if is_repack_exempt(dockerfile):
            continue

        ep_raw, ep_args = parse_dockerfile_entrypoint(dockerfile)

        # Check if this image has the bug (ENTRYPOINT with "run" but no "-c")
        if not ep_args or len(ep_args) < 2:
            continue

        if ep_args[1] != "run":
            continue  # Not a shim run entrypoint

        has_c = len(ep_args) >= 4 and ep_args[2] == "-c"
        if has_c:
            already_ok += 1
            continue

        # This image has the bug — find the binary from manifest
        binary = parse_manifest_entrypoint(manifest)

        if binary:
            if fix_entrypoint(dockerfile, binary):
                fixed += 1
            else:
                errors.append(f"{img}: couldn't replace ENTRYPOINT (pattern not found)")
        else:
            # Try CMD as fallback
            cmd_raw, cmd_args = parse_dockerfile_cmd(dockerfile)
            if cmd_args:
                # Use CMD as the binary command
                binary = " ".join(cmd_args)
                if fix_entrypoint(dockerfile, binary):
                    fixed += 1
                else:
                    errors.append(f"{img}: couldn't replace ENTRYPOINT")
            else:
                no_manifest += 1
                errors.append(f"{img}: no entrypoint in manifest.toml and no CMD")

    print("\n=== ENTRYPOINT Fix Results ===")
    print(f"✅ Fixed:            {fixed}")
    print(f"✅ Already OK:       {already_ok}")
    print(f"❌ No entrypoint:    {no_manifest}")
    print(f"Errors:              {len(errors)}")

    if errors:
        print("\nNeed manual fix:")
        for e in errors[:20]:
            print(f"  {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")

    return fixed, errors


if __name__ == "__main__":
    main()
