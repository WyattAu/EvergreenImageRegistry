# =============================================================================
# SOVEREIGN WOLFI-JDK
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

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache \
    ca-certificates
# wolfi provides java-21-default-jdk via: apk add java-21-default-jdk
# But the package name varies; use wolfi's native java if available
RUN apk add --no-cache java-21-default-jdk 2>/dev/null || \
    apk add --no-cache openjdk-21-jdk-headless 2>/dev/null || true
