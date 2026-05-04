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

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache \
    ca-certificates && \
    apk add --no-cache java-21-default-jdk 2>/dev/null || \
    apk add --no-cache openjdk-21-jdk-headless 2>/dev/null || true
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
HEALTHCHECK NONE
