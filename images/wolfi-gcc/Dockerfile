# =============================================================================
# SOVEREIGN WOLFI-GCC
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

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache \
    gcc g++ cpp \
    make cmake autoconf automake libtool \
    pkgconfig \
    zlib-dev openssl-dev \
    bison flex \
    git ca-certificates bash
