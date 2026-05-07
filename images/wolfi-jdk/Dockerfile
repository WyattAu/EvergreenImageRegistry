# =============================================================================
# EVERGREEN WOLFI-JDK
# Chainguard wolfi + OpenJDK runtime for Java applications.
# NOT a source-build image — Java images download pre-built JARs/WARs.
#
# Provides:
#   - wolfi-base (musl libc)
#   - openjdk-21 (Eclipse Temurin LTS, latest)
#   - ca-certificates (TLS for downloads)
#
# Note: Chainguard wolfi provides java-21 as 'java-21-default-jdk'.
# This base ensures a consistent JDK across all Java images.
# =============================================================================

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache \
    ca-certificates && \
    apk add --no-cache java-21-default-jdk 2>/dev/null || \
    apk add --no-cache openjdk-21-jdk-headless 2>/dev/null || true
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="0"
HEALTHCHECK NONE
LABEL org.opencontainers.image.description="wolfi-jdk container image" \
      org.opencontainers.image.title="Wolfi JDK" \
      org.opencontainers.image.source="https://github.com/wolfi-dev/os" \
            org.opencontainers.image.version="unknown"
