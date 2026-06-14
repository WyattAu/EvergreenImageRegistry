# =============================================================================
# EVERGREEN HARDENED OPENHAB
# Generated from template - Version: 4.3.11
# Downloads OpenHAB distribution directly from GitHub releases (no upstream image).
# OpenHAB is a Java application; uses wolfi-jdk base for JDK runtime.
# =============================================================================

ARG VERSION=5.2.0.M3
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=5.2.0.M3
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/openhab/openhab-distro/releases/download/${VERSION}/openhab-${VERSION}.tar.gz" -o /tmp/openhab.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/openhab.tar.gz -C /app && rm -f /tmp/openhab.tar.gz && \
    chmod +x /app/start.sh
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl 2>/dev/null && \
    apk add --no-cache java-21-default-jdk 2>/dev/null || \
    apk add --no-cache openjdk-21-jdk-headless 2>/dev/null && \
    adduser -u 65532 -D openhab 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /openhab
RUN mkdir -p /openhab/conf /openhab/userdata /var/log/openhab /var/cache/openhab && \
    chown -R 65532:65532 /openhab/conf /openhab/userdata /var/log/openhab /var/cache/openhab 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /openhab

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
EXPOSE 8080 8443

LABEL org.opencontainers.image.title="openhab" \
      org.opencontainers.image.description="openhab container image" \
      org.opencontainers.image.version="4.3.11" \
      org.opencontainers.image.vendor="OpenHAB" \
      org.opencontainers.image.source="https://github.com/openhab/openhab-distro" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.official="true"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
