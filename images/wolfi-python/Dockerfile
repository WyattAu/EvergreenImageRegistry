# =============================================================================
# SOVEREIGN WOLFI-PYTHON
# Chainguard wolfi + Python runtime for Python applications.
#
# Provides:
#   - wolfi-base (musl libc)
#   - python3, pip (Python runtime and package manager)
#   - git, ca-certificates (source fetching)
#   - build-base (for packages with C extensions)
# =============================================================================

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache \
    python3 py3-pip \
    git ca-certificates bash \
    build-base
