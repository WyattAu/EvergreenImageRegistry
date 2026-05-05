# =============================================================================
# EVERGREEN WOLFI-PYTHON
# Chainguard wolfi + Python runtime for Python applications.
#
# Provides:
#   - wolfi-base (musl libc)
#   - python3, pip (Python runtime and package manager)
#   - git, ca-certificates (source fetching)
#   - build-base (for packages with C extensions)
# =============================================================================

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache \
    python3 py3-pip \
    git ca-certificates bash \
    build-base

LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="0"
HEALTHCHECK NONE
LABEL org.opencontainers.image.description="wolfi-python container image" \
      org.opencontainers.image.title="Wolfi Python" \
      org.opencontainers.image.source="https://github.com/wolfi-dev/os" \
            org.opencontainers.image.version="unknown"
