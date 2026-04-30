# =============================================================================
# SOVEREIGN WOLFI-NODE
# Chainguard wolfi + Node.js runtime for source-build Node apps.
#
# Provides:
#   - wolfi-base (musl libc)
#   - nodejs, npm (Node.js runtime and package manager)
#   - git, ca-certificates (source fetching)
# =============================================================================

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache \
    nodejs npm \
    git ca-certificates bash
