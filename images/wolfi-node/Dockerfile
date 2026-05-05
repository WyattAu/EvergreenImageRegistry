# =============================================================================
# EVERGREEN WOLFI-NODE
# Chainguard wolfi + Node.js runtime for source-build Node apps.
#
# Provides:
#   - wolfi-base (musl libc)
#   - nodejs, npm (Node.js runtime and package manager)
#   - git, ca-certificates (source fetching)
# =============================================================================

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
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
      org.opencontainers.image.source="https://github.com/wolfi-dev/os" \
            org.opencontainers.image.version="unknown"
