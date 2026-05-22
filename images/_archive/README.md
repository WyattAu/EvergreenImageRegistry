# Archived Images

Images moved here have Dockerfile parse errors, broken shell continuations,
or other structural issues that prevent them from building. They are retained
for reference but are excluded from CI build pipelines.

## Status

These images will not be built by any CI workflow. To restore an image:

1. Fix the Dockerfile issue
2. Move from `_archive/` back to `images/`
3. Ensure it passes `hadolint` and the Evergreen constraints check

## Archived On

2026-05-22: 47 images archived due to broken shell continuations (missing
backslashes after RUN/COPY lines) and Dockerfile parse errors identified
during Path C quality-first rebuild static triage.

2026-05-22: keynuker archived - upstream GitHub repo (clonezilla/keynuker) no
longer exists (404). GHCR image inaccessible.

2026-05-22: statuspage archived - upstream cstate is a Hugo theme/nginx image,
not a standalone binary. GHCR image not publicly accessible (denied).
