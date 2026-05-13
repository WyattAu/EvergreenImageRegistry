#!/usr/bin/env python3

import glob
import os
import re

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "images")


def find_last_from_index(lines):
    last_from = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r"^FROM\s+", stripped, re.IGNORECASE):
            last_from = i
    return last_from


def replace_uid_in_final_stage(content):
    lines = content.split("\n")
    last_from = find_last_from_index(lines)

    if last_from < 0:
        return content, 0

    replacements = 0

    for i in range(last_from + 1, len(lines)):
        original = lines[i]
        modified = original

        modified = re.sub(r"\bUSER\s+65534(:65534)?\b", "USER 65532:65532", modified)
        modified = re.sub(r"(--uid\s+)65534\b", r"\g<1>65532", modified)
        modified = re.sub(r"(--gid\s+)65534\b", r"\g<1>65532", modified)
        modified = re.sub(r"(--chown=)65534:65534\b", r"\g<1>65532:65532", modified)
        modified = re.sub(
            r"(chown\s+-R\s+)65534:65534\b", r"\g<1>65532:65532", modified
        )
        modified = re.sub(r"(usermod\s+-u\s+)65534\b", r"\g<1>65532", modified)
        modified = re.sub(r"\b(-[ug]\s+)65534\b", r"\g<1>65532", modified)
        modified = re.sub(r"\b(addgroup\s+-g\s+)65534\b", r"\g<1>65532", modified)
        modified = re.sub(
            r"\b(adduser\s+-[DG]\s+-u\s+)65534\b", r"\g<1>65532", modified
        )
        modified = re.sub(r"\b(adduser\s+-[DG]\s+)65534\b", r"\g<1>65532", modified)
        modified = re.sub(r"\b65534:65534\b", "65532:65532", modified)
        modified = re.sub(r"\b65534\b", "65532", modified)

        if modified != original:
            replacements += 1

        lines[i] = modified

    return "\n".join(lines), replacements


def main():
    pattern = os.path.join(IMAGES_DIR, "*", "Dockerfile")
    dockerfiles = sorted(glob.glob(pattern))

    files_modified = 0
    total_replacements = 0

    for filepath in dockerfiles:
        with open(filepath) as f:
            content = f.read()

        new_content, replacements = replace_uid_in_final_stage(content)

        if replacements > 0:
            with open(filepath, "w") as f:
                f.write(new_content)
            files_modified += 1
            total_replacements += replacements
            print(f"  {filepath}: {replacements} replacement(s)")

    print(f"\nFiles modified: {files_modified}")
    print(f"Total replacements: {total_replacements}")


if __name__ == "__main__":
    main()
