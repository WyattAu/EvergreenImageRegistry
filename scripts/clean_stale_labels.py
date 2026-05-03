#!/usr/bin/env python3
"""Clean up stale labels from Dockerfiles in the EvergreenImageRegistry project."""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def find_dockerfiles():
    result = subprocess.run(
        ["git", "ls-files", "--", "*/Dockerfile*"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return [ROOT / p for p in result.stdout.strip().splitlines() if p]


def get_final_stage_base(content: str) -> str:
    from_lines = [
        line
        for line in content.splitlines()
        if line.strip().upper().startswith("FROM ")
    ]
    if not from_lines:
        return "unknown"
    last_from = from_lines[-1].strip()
    lower = last_from.lower()
    if "scratch" in lower:
        return "scratch"
    if "wolfi" in lower or "chainguard" in lower:
        return "wolfi"
    if "ubi" in lower or "redhat" in lower:
        return "rhel-ubi"
    image_part = last_from.split(maxsplit=1)[1]
    image_part = re.sub(r"\s+AS\s+.*", "", image_part, flags=re.IGNORECASE)
    image_part = image_part.split("/")[0].split(":")[0]
    return image_part


def remove_debian_slim_label(content: str) -> tuple[str, int]:
    count = 0
    lines = content.splitlines(keepends=True)
    new_lines = []
    for line in lines:
        if "evergreen.constraint.debian_slim" in line:
            count += 1
            stripped = line.rstrip("\n\r")
            rstripped = stripped.rstrip()
            if rstripped.endswith("\\"):
                new_lines.append(rstripped.removesuffix("\\").rstrip() + "\n")
            else:
                continue
        else:
            new_lines.append(line)
    return "".join(new_lines), count


def fix_base_label(content: str) -> tuple[str, str | None]:
    match = re.search(
        r'evergreen\.constraint\.base="(debian-slim|alpine)"',
        content,
    )
    if not match:
        return content, None
    actual_base = get_final_stage_base(content)
    old_val = match.group(1)
    new_content = re.sub(
        r'evergreen\.constraint\.base="(debian-slim|alpine)"',
        f'evergreen.constraint.base="{actual_base}"',
        content,
    )
    return new_content, actual_base


def main():
    dockerfiles = find_dockerfiles()
    total_debian_slim_removed = 0
    base_updates: dict[str, int] = {}
    could_not_fix: list[str] = []

    for df in sorted(dockerfiles):
        original = df.read_text()
        content = original
        changed = False

        content, removed = remove_debian_slim_label(content)
        if removed:
            total_debian_slim_removed += removed
            changed = True

        content, new_base = fix_base_label(content)
        if new_base is not None:
            changed = True
            if new_base in ("unknown",) or new_base not in (
                "scratch",
                "wolfi",
                "rhel-ubi",
            ):
                could_not_fix.append(
                    f"{df.relative_to(ROOT)}: set to '{new_base}' (needs review)"
                )
            base_updates[new_base] = base_updates.get(new_base, 0) + 1

        if changed:
            df.write_text(content)

    print(f"=== evergreen.constraint.debian_slim ===")
    print(f"Removed {total_debian_slim_removed} lines across all Dockerfiles")
    print()
    print(f"=== evergreen.constraint.base ===")
    print(f"Updated {sum(base_updates.values())} values:")
    for base, count in sorted(base_updates.items()):
        print(f"  {base}: {count}")
    print()
    if could_not_fix:
        print(f"=== Files needing manual review ({len(could_not_fix)}) ===")
        for f in could_not_fix:
            print(f"  {f}")
    else:
        print("All files fixed successfully.")


if __name__ == "__main__":
    main()
