#!/usr/bin/env python3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"

total_modified = 0
total_blocks_removed = 0
needs_review = []


def remove_healthcheck_lines(lines):
    global total_blocks_removed
    result = []
    i = 0
    blocks_removed = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("HEALTHCHECK"):
            blocks_removed += 1
            i += 1
            while i < len(lines):
                s = lines[i].rstrip()
                if s.endswith("\\"):
                    i += 1
                else:
                    i += 1
                    break
            continue
        result.append(lines[i])
        i += 1

    if blocks_removed > 0:
        total_blocks_removed += blocks_removed
        cleaned = []
        prev_blank = False
        for line in result:
            if line.strip() == "":
                if prev_blank:
                    continue
                prev_blank = True
                cleaned.append(line)
            else:
                prev_blank = False
                cleaned.append(line)
        while cleaned and cleaned[0].strip() == "":
            cleaned.pop(0)
        while cleaned and cleaned[-1].strip() == "":
            cleaned.pop()
        return cleaned, blocks_removed
    return result, 0


def main():
    global total_modified, total_blocks_removed

    dockerfiles = sorted(IMAGES_DIR.glob("*/Dockerfile"))
    for df in dockerfiles:
        content = df.read_text()
        original = content
        lines = content.split("\n")
        cleaned, removed = remove_healthcheck_lines(lines)
        new_content = "\n".join(cleaned) if removed > 0 else original
        if removed > 0:
            if new_content != original:
                df.write_text(new_content)
                total_modified += 1
            else:
                needs_review.append(
                    f"{df}: HEALTHCHECK found but content unchanged after removal"
                )
        if "\n\n\n" in new_content:
            needs_review.append(f"{df}: contains triple newlines after cleanup")

    logger.info(f"Total Dockerfiles modified: {total_modified}")
    logger.info(f"Total HEALTHCHECK blocks removed: {total_blocks_removed}")
    if needs_review:
        logger.info(f"Files needing manual review ({len(needs_review)}):")
        for f in needs_review:
            logger.info(f"- {f}")
    else:
        logger.info("No files need manual review.")

    remaining = sum(
        1
        for df in dockerfiles
        if "HEALTHCHECK" in df.read_text().split("\n")
        and any(
            line.strip().startswith("HEALTHCHECK")
            for line in df.read_text().split("\n")
        )
    )
    if remaining:
        logger.warning(
            f"{remaining} Dockerfiles still contain HEALTHCHECK instructions!"
        )
    else:
        logger.info(
            "Verification: No HEALTHCHECK instructions remain in any Dockerfile."
        )


if __name__ == "__main__":
    main()
