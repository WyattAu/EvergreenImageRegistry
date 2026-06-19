#!/usr/bin/env python3
"""Validate EIR images follow the standard ENTRYPOINT/CMD pattern.

Standard patterns:
  ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/path/to/binary"]  # with wrapper
  ENTRYPOINT ["/usr/local/bin/shim", "run", "/path/to/binary"]         # without wrapper
  CMD ["<arg1>", "<arg2>"]  # Only args, no binary name, no -c flag

Usage:
    python scripts/validate_entrypoint_pattern.py [--fix] [--image NAME]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"

# Canonical shim path
SHIM_PATH_CANONICAL = "/usr/local/bin/shim"
# Deprecated shim path (scratch images should use canonical)
SHIM_PATH_DEPRECATED = "/shim"
# All known shim paths for backwards compatibility in parsing
SHIM_PATHS = (SHIM_PATH_CANONICAL, SHIM_PATH_DEPRECATED)


class PatternResult(NamedTuple):
    image: str
    has_shim_copy: bool
    shim_path: str | None
    shim_path_correct: bool
    entrypoint_correct: bool
    entrypoint_raw: str
    entrypoint_has_c_flag: bool
    cmd_correct: bool
    cmd_raw: str
    issues: list[str]


def parse_dockerfile(path: Path) -> dict[str, list[str]]:
    """Parse a Dockerfile into stages with their instructions."""
    stages: dict[str, list[str]] = {"_all": []}
    current_stage = "_all"

    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.upper().startswith("FROM "):
            parts = stripped.split()
            if len(parts) >= 2 and "AS" in stripped.upper():
                as_idx = next(i for i, p in enumerate(parts) if p.upper() == "AS")
                current_stage = parts[as_idx + 1]
            else:
                current_stage = stripped
            stages.setdefault(current_stage, [])

        stages.setdefault(current_stage, []).append(stripped)
        stages["_all"].append(stripped)

    return stages


def is_scratch_image(dockerfile_text: str) -> bool:
    """Check if the final stage uses scratch as the base image."""
    for line in dockerfile_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("FROM "):
            parts = stripped.split()
            image = parts[1] if len(parts) >= 2 else ""
            if image == "scratch":
                return True
    return False


def find_shim_copy(dockerfile_text: str) -> tuple[bool, str | None]:
    """Check for COPY --from=shim instruction. Returns (found, destination_path)."""
    for line in dockerfile_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("COPY") and "--FROM=SHIM" in stripped.upper():
            parts = stripped.split()
            for i, part in enumerate(parts):
                if part.upper() == "--FROM=SHIM":
                    # COPY --from=shim SOURCE DEST — dest is two positions after --from=shim
                    dest = parts[i + 2] if i + 2 < len(parts) else None
                    return True, dest
    return False, None


def find_entrypoint(dockerfile_text: str) -> tuple[str | None, list[str]]:
    """Find ENTRYPOINT instruction and parse its arguments."""
    for line in dockerfile_text.splitlines():
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


def find_cmd(dockerfile_text: str) -> tuple[str | None, list[str]]:
    """Find CMD instruction and parse its arguments."""
    for line in dockerfile_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("CMD"):
            content = stripped[len("CMD") :].strip()
            match = re.match(r"\[(.*)\]", content)
            if match:
                args = [
                    a.strip().strip('"').strip("'") for a in match.group(1).split(",")
                ]
                return content, args
            return content, content.split()
    return None, []


def validate_image(image_name: str) -> PatternResult:
    """Validate a single image follows the standard pattern."""
    dockerfile = IMAGES_DIR / image_name / "Dockerfile"
    if not dockerfile.exists():
        return PatternResult(
            image=image_name,
            has_shim_copy=False,
            shim_path=None,
            shim_path_correct=False,
            entrypoint_correct=False,
            entrypoint_raw="",
            entrypoint_has_c_flag=False,
            cmd_correct=False,
            cmd_raw="",
            issues=["Dockerfile not found"],
        )

    text = dockerfile.read_text()
    issues = []

    # Check for repack-upstream-init exemption label
    # Images with upstream init systems (s6, tini) keep upstream ENTRYPOINT
    # and use shim only for HEALTHCHECK. Marked with:
    #   LABEL evergreen.entrypoint.pattern="repack-upstream-init"
    is_repack_init = (
        'evergreen.entrypoint.pattern="repack-upstream-init"' in text
        or "evergreen.entrypoint.pattern='repack-upstream-init'" in text
        or 'evergreen.entrypoint.pattern = "repack-upstream-init"' in text
    )

    has_copy, shim_path = find_shim_copy(text)
    if not has_copy:
        issues.append("Missing COPY --from=shim instruction")

    # Check shim path: scratch-based images must use /usr/local/bin/shim
    scratch = is_scratch_image(text)
    shim_path_correct = True
    if scratch and shim_path and shim_path != SHIM_PATH_CANONICAL:
        shim_path_correct = False
        issues.append(
            f"Scratch image uses deprecated shim path '{shim_path}', "
            f"expected '{SHIM_PATH_CANONICAL}'"
        )

    ep_raw, ep_args = find_entrypoint(text)
    cmd_raw, cmd_args = find_cmd(text)

    entrypoint_correct = False
    entrypoint_has_c_flag = False
    if ep_args:
        if is_repack_init:
            # Repack images with upstream init (s6, tini) keep upstream ENTRYPOINT
            # Shim is only used for HEALTHCHECK, not as process supervisor
            entrypoint_correct = True
            entrypoint_has_c_flag = True  # Exempt from -c requirement
        elif (
            len(ep_args) >= 3
            and ep_args[0] == SHIM_PATH_CANONICAL
            and ep_args[1] == "run"
        ):
            entrypoint_correct = True
            entrypoint_has_c_flag = len(ep_args) >= 4 and ep_args[2] == "-c"
        else:
            issues.append(f"ENTRYPOINT does not follow standard: {ep_raw}")
    elif is_repack_init:
        # Repack image that inherits ENTRYPOINT from upstream (no explicit ENTRYPOINT)
        entrypoint_correct = True
        entrypoint_has_c_flag = True
    else:
        issues.append("No ENTRYPOINT found")

    # For scratch images, ENTRYPOINT must have -c flag
    if scratch and not entrypoint_has_c_flag and entrypoint_correct:
        issues.append("Scratch image ENTRYPOINT missing -c flag")

    cmd_correct = False
    if is_repack_init:
        # Repack images may have any CMD format (delegating to upstream init)
        cmd_correct = True
    elif cmd_args:
        # Standard: only args, no binary name, no -c flag
        binary_name = ""
        if len(ep_args) >= 3:
            binary_path = (
                ep_args[2]
                if ep_args[2] != "-c" and len(ep_args) >= 4
                else ep_args[-1]
                if len(ep_args) >= 3
                else ""
            )
            binary_name = binary_path.split("/")[-1] if binary_path else ""

        has_c_flag = cmd_args[0] == "-c" if cmd_args else False
        has_binary = (
            any(binary_name in arg for arg in cmd_args) if binary_name else False
        )

        if not has_c_flag and not has_binary:
            cmd_correct = True
        else:
            issues.append(f"CMD contains binary name or -c flag: {cmd_raw}")
    elif not cmd_args:
        cmd_correct = True

    return PatternResult(
        image=image_name,
        has_shim_copy=has_copy,
        shim_path=shim_path,
        shim_path_correct=shim_path_correct,
        entrypoint_correct=entrypoint_correct,
        entrypoint_raw=ep_raw or "",
        entrypoint_has_c_flag=entrypoint_has_c_flag,
        cmd_correct=cmd_correct,
        cmd_raw=cmd_raw or "",
        issues=issues,
    )


def fix_dockerfile(image_name: str, dry_run: bool = True) -> list[str]:
    """Fix common issues in a Dockerfile. Returns list of changes made."""
    dockerfile = IMAGES_DIR / image_name / "Dockerfile"
    if not dockerfile.exists():
        return []

    text = dockerfile.read_text()
    original = text
    changes = []

    # Fix: Standardize shim path for scratch images
    if is_scratch_image(text):
        # Fix COPY --from=shim destination
        if f"COPY --from=shim /shim {SHIM_PATH_DEPRECATED}" in text:
            text = text.replace(
                f"COPY --from=shim /shim {SHIM_PATH_DEPRECATED}",
                f"COPY --from=shim /shim {SHIM_PATH_CANONICAL}",
            )
            changes.append(f"Standardized COPY destination to {SHIM_PATH_CANONICAL}")

        # Fix ENTRYPOINT shim path
        for old_path in SHIM_PATHS:
            if old_path != SHIM_PATH_CANONICAL:
                text = text.replace(
                    f'"{old_path}", "run"', f'"{SHIM_PATH_CANONICAL}", "run"'
                )

        # Fix HEALTHCHECK shim path
        for old_path in SHIM_PATHS:
            if old_path != SHIM_PATH_CANONICAL:
                text = text.replace(
                    f'"{old_path}", "healthcheck"',
                    f'"{SHIM_PATH_CANONICAL}", "healthcheck"',
                )

    # Fix: Remove -c flag from CMD if ENTRYPOINT already has it
    lines = text.splitlines()
    new_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("CMD") and stripped.upper() != "CMD-SHELL":
            match = re.match(r"CMD\s+\[(.*)\]", stripped)
            if match:
                args = [
                    a.strip().strip('"').strip("'") for a in match.group(1).split(",")
                ]
                if args and args[0] == "-c":
                    args = args[1:]
                    if args and "/" in args[0]:
                        args = args[1:]
                    if args:
                        new_cmd = "[" + ", ".join(f'"{a}"' for a in args) + "]"
                    else:
                        new_cmd = "[]"
                    new_line = line.replace(match.group(0), f"CMD {new_cmd}")
                    new_lines.append(new_line)
                    changes.append("Removed -c flag and binary name from CMD")
                    continue
        new_lines.append(line)

    text = "\n".join(new_lines)

    if text != original:
        if not dry_run:
            dockerfile.write_text(text)
        return changes

    return []


def main():
    parser = argparse.ArgumentParser(description="Validate EIR ENTRYPOINT/CMD patterns")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues")
    parser.add_argument("--image", type=str, help="Check a specific image")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.image:
        images = [args.image]
    else:
        images = sorted(
            d.name
            for d in IMAGES_DIR.iterdir()
            if d.is_dir()
            and not d.name.startswith("_")
            and not d.name.startswith(".")
            and (d / "Dockerfile").exists()
        )

    results = []
    total = 0
    passing = 0
    failing = 0
    shim_issues = 0

    for img in images:
        result = validate_image(img)
        results.append(result)
        total += 1

        if result.issues:
            failing += 1
            if not result.shim_path_correct:
                shim_issues += 1
        else:
            passing += 1

        if args.fix and result.issues:
            changes = fix_dockerfile(img, dry_run=False)
            if changes:
                print(f"[FIXED] {img}: {', '.join(changes)}")

    if args.json:
        import json

        output = {
            "total": total,
            "passing": passing,
            "failing": failing,
            "shim_path_issues": shim_issues,
            "results": [r._asdict() for r in results],
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n=== EIR Entrypoint Pattern Validation ===")
        print(
            f"Total: {total} | Passing: {passing} | Failing: {failing} | Shim path issues: {shim_issues}\n"
        )

        if failing > 0:
            print("FAILURES:")
            for r in results:
                if r.issues:
                    print(f"  {r.image}:")
                    for issue in r.issues:
                        print(f"    - {issue}")
            print()

    sys.exit(1 if failing > 0 else 0)


if __name__ == "__main__":
    main()
