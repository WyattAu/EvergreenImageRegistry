# =============================================================================
# EVERGREEN WOLFI-GCC
# Chainguard wolfi + build toolchain (gcc, g++, make, cmake, autoconf)
# For images that compile C/C++ from source.
#
# Provides:
#   - wolfi-base (musl libc, no glibc)
#   - gcc, g++, cpp (C/C++ compilers)
#   - make, cmake, autoconf, automake, libtool (build systems)
#   - pkg-config, zlib, openssl-dev (common build deps)
#   - git, ca-certificates (source fetching)
#   - bash (build scripts)
# =============================================================================

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache \
    gcc  \
    make cmake autoconf automake libtool \
    pkgconf \
    zlib-dev openssl-dev \
    bison flex \
    git ca-certificates bash

LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="0"
HEALTHCHECK NONE
LABEL org.opencontainers.image.description="wolfi-gcc container image" \
      org.opencontainers.image.title="Wolfi GCC" \
      org.opencontainers.image.source="https://github.com/wolfi-dev/os" \
            org.opencontainers.image.version="unknown"
