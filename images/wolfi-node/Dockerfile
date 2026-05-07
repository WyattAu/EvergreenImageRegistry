# =============================================================================
# EVERGREEN WOLFI-NODE
# Chainguard wolfi + Node.js runtime for source-build Node apps.
#
# Provides:
#   - wolfi-base (musl libc)
#   - nodejs, npm (Node.js runtime and package manager)
#   - git, ca-certificates (source fetching)
# =============================================================================

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache \
    nodejs npm \
    git ca-certificates bash

LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="0"
HEALTHCHECK NONE
LABEL org.opencontainers.image.description="wolfi-node container image" \
      org.opencontainers.image.title="Wolfi Node.js" \
      org.opencontainers.image.source="https://github.com/wolfi-dev/os" \
            org.opencontainers.image.version="unknown"
