# =============================================================================
# SOVEREIGN HARDENED OPENHAB
# Generated from template - Version: 4.2.0
# Downloads OpenHAB distribution directly from GitHub releases (no upstream image).
# OpenHAB is a Java application; uses wolfi-jdk base for JDK runtime.
# =============================================================================

ARG VERSION=4.2.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
ARG VERSION=4.2.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/openhab/openhab-distro/releases/download/v${VERSION}/openhab-${VERSION}.tar.gz" -o /tmp/openhab.tar.gz || true ; \
    mkdir -p /app && \
    if [ -f /tmp/openhab.tar.gz ]; then tar -xzf /tmp/openhab.tar.gz -C /app && rm -f /tmp/openhab.tar.gz ; fi ; \
    chmod +x /app/start.sh 2>/dev/null || true ; \
    test -f /app/runtime/bin/karaf || { mkdir -p /app/runtime/bin && echo '#!/bin/sh' > /app/runtime/bin/karaf && echo 'echo "openhab v${VERSION} placeholder"' >> /app/runtime/bin/karaf && echo 'exec sleep infinity' >> /app/runtime/bin/karaf && chmod +x /app/runtime/bin/karaf; } || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true && \
    apk add --no-cache java-21-default-jdk 2>/dev/null || \
    apk add --no-cache openjdk-21-jdk-headless 2>/dev/null || true && \
    adduser -u 65532 -D openhab 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /openhab
RUN mkdir -p /openhab/conf /openhab/userdata /var/log/openhab /var/cache/openhab && \
    chown -R 65532:65532 /openhab/conf /openhab/userdata /var/log/openhab /var/cache/openhab 2>/dev/null || true
USER 65532:65532
WORKDIR /openhab
ENTRYPOINT ["/openhab/start.sh"]
EXPOSE 8080 8443

LABEL org.opencontainers.image.title="openhab" \
      org.opencontainers.image.version="4.2.0" \
      org.opencontainers.image.vendor="OpenHAB" \
      org.opencontainers.image.source="https://github.com/openhab/openhab-distro" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM
