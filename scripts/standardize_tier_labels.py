#!/usr/bin/env python3
"""
Standardize tier labels across all manifests.

Ensures every manifest.toml has both:
- [metadata] tier = "..." (the source of truth)
- [labels] "evergreen.image.tier" = "..." (for Dockerfile generation)

Usage:
    python3 scripts/standardize_tier_labels.py [--dry-run]
"""

import sys
from pathlib import Path

import tomllib


def main():
    dry_run = "--dry-run" in sys.argv
    images_dir = Path("images")
    exclude_dirs = {"_wip", "_archive", "tests"}

    image_dirs = sorted(
        [d for d in images_dir.iterdir() if d.is_dir() and d.name not in exclude_dirs]
    )

    fixed = 0
    already_ok = 0
    errors = 0

    for d in image_dirs:
        mf_path = d / "manifest.toml"
        if not mf_path.exists():
            continue

        try:
            content = mf_path.read_text()
            with open(mf_path, "rb") as f:
                data = tomllib.load(f)
        except Exception as e:
            print(f"ERROR: {d.name}: {e}")
            errors += 1
            continue

        # Get tier from metadata (source of truth)
        tier = data.get("metadata", {}).get("tier", "")
        if not tier:
            print(f"WARN: {d.name}: no tier in metadata, skipping")
            continue

        # Check if labels section has evergreen.image.tier
        labels = data.get("labels", {})
        _expected_label = f'"evergreen.image.tier" = "{tier}"'

        if labels.get("evergreen.image.tier") == tier:
            already_ok += 1
            continue

        # Need to add or fix the label
        if dry_run:
            print(f'DRY-RUN: {d.name}: would add/fix evergreen.image.tier = "{tier}"')
            fixed += 1
            continue

        # Add the label to the [labels] section
        if "[labels]" in content:
            # Add after [labels] line
            lines = content.split("\n")
            new_lines = []
            labels_section_found = False
            tier_label_added = False

            for line in lines:
                new_lines.append(line)
                if line.strip() == "[labels]":
                    labels_section_found = True
                elif (
                    labels_section_found
                    and not tier_label_added
                    and line.strip().startswith("[")
                ):
                    # Next section, insert before it
                    new_lines.pop()  # Remove the section header
                    new_lines.append(f'"evergreen.image.tier" = "{tier}"')
                    new_lines.append("")  # Blank line
                    new_lines.append(line)  # Re-add section header
                    tier_label_added = True

            if not tier_label_added:
                # Append at end
                new_lines.append(f'"evergreen.image.tier" = "{tier}"')

            mf_path.write_text("\n".join(new_lines))
        else:
            # No labels section, add one
            content += f'\n[labels]\n"evergreen.image.tier" = "{tier}"\n'
            mf_path.write_text(content)

        fixed += 1
        print(f'FIXED: {d.name}: added evergreen.image.tier = "{tier}"')

    print(f"\nSummary: {already_ok} OK, {fixed} fixed, {errors} errors")


if __name__ == "__main__":
    main()
