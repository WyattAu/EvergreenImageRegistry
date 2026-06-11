#!/usr/bin/env python3
"""Validate EIR images follow the standard ENTRYPOINT/CMD pattern.

Standard patterns:
  ENTRYPOINT ["/shim", "run", "-c", "/path/to/binary"]  # with wrapper
  ENTRYPOINT ["/shim", "run", "/path/to/binary"]         # without wrapper
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

# Known shim paths
SHIM_PATHS = ("/shim", "/usr/local/bin/shim")


class PatternResult(NamedTuple):
    image: str
    has_shim_copy: bool
    shim_path: str | None
    entrypoint_correct: bool
    entrypoint_raw: str
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


def find_shim_copy(dockerfile_text: str) -> tuple[bool, str | None]:
    """Check for COPY --from=shim instruction."""
    for line in dockerfile_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("COPY") and "--FROM=SHIM" in stripped.upper():
            parts = stripped.split()
            for i, part in enumerate(parts):
                if part.upper() == "--FROM=SHIM":
                    dest = parts[i + 1] if i + 1 < len(parts) else None
                    return True, dest
    return False, None


def find_entrypoint(dockerfile_text: str) -> tuple[str | None, list[str]]:
    """Find ENTRYPOINT instruction and parse its arguments."""
    for line in dockerfile_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("ENTRYPOINT"):
            content = stripped[len("ENTRYPOINT"):].strip()
            match = re.match(r'\[(.*)\]', content)
            if match:
                args = [a.strip().strip('"').strip("'") for a in match.group(1).split(",")]
                return content, args
            return content, content.split()
    return None, []


def find_cmd(dockerfile_text: str) -> tuple[str | None, list[str]]:
    """Find CMD instruction and parse its arguments."""
    for line in dockerfile_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("CMD"):
            content = stripped[len("CMD"):].strip()
            match = re.match(r'\[(.*)\]', content)
            if match:
                args = [a.strip().strip('"').strip("'") for a in match.group(1).split(",")]
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
            entrypoint_correct=False,
            entrypoint_raw="",
            cmd_correct=False,
            cmd_raw="",
            issues=["Dockerfile not found"],
        )

    text = dockerfile.read_text()
    issues = []

    has_copy, shim_path = find_shim_copy(text)
    if not has_copy:
        issues.append("Missing COPY --from=shim instruction")

    ep_raw, ep_args = find_entrypoint(text)
    cmd_raw, cmd_args = find_cmd(text)

    entrypoint_correct = False
    if ep_args:
        # Pattern 1: ["/shim", "run", "-c", "<binary>"]
        # Pattern 2: ["/shim", "run", "<binary>"]
        # Pattern 3: ["/usr/local/bin/shim", "run", "-c", "<binary>"]
        # Pattern 4: ["/usr/local/bin/shim", "run", "<binary>"]
        if (
            len(ep_args) >= 3
            and ep_args[0] in SHIM_PATHS
            and ep_args[1] == "run"
        ):
            entrypoint_correct = True
        else:
            issues.append(f"ENTRYPOINT does not follow standard: {ep_raw}")
    else:
        issues.append("No ENTRYPOINT found")

    cmd_correct = False
    if cmd_args:
        # Standard: only args, no binary name, no -c flag
        # Extract binary name from ENTRYPOINT
        binary_name = ""
        if len(ep_args) >= 3:
            binary_path = ep_args[2] if ep_args[2] != "-c" and len(ep_args) >= 4 else ep_args[-1] if len(ep_args) >= 3 else ""
            binary_name = binary_path.split("/")[-1] if binary_path else ""

        has_c_flag = cmd_args[0] == "-c" if cmd_args else False
        has_binary = any(binary_name in arg for arg in cmd_args) if binary_name else False

        if not has_c_flag and not has_binary:
            cmd_correct = True
        else:
            issues.append(f"CMD contains binary name or -c flag: {cmd_raw}")
    elif not cmd_args:
        # CMD is acceptable if ENTRYPOINT provides all arguments
        cmd_correct = True

    return PatternResult(
        image=image_name,
        has_shim_copy=has_copy,
        shim_path=shim_path,
        entrypoint_correct=entrypoint_correct,
        entrypoint_raw=ep_raw or "",
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

    # Fix: Remove -c flag from CMD if ENTRYPOINT already has it
    lines = text.splitlines()
    new_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("CMD") and stripped.upper() != "CMD-SHELL":
            match = re.match(r'CMD\s+\[(.*)\]', stripped)
            if match:
                args = [a.strip().strip('"').strip("'") for a in match.group(1).split(",")]
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
            d.name for d in IMAGES_DIR.iterdir()
            if d.is_dir()
            and not d.name.startswith("_")
            and not d.name.startswith(".")
            and (d / "Dockerfile").exists()
        )

    results = []
    total = 0
    passing = 0
    failing = 0

    for img in images:
        result = validate_image(img)
        results.append(result)
        total += 1

        if result.issues:
            failing += 1
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
            "results": [r._asdict() for r in results],
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n=== EIR Entrypoint Pattern Validation ===")
        print(f"Total: {total} | Passing: {passing} | Failing: {failing}\n")

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
