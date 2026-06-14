# =============================================================================
# EVERGREEN HARDENED SONARR
# Generated from template - Version: 4.0.10
# Downloads Sonarr binary directly from GitHub releases (no upstream image).
# Sonarr is a .NET application; uses wolfi base for glibc/runtime.
# =============================================================================

ARG VERSION=4.0.17.2952
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=4.0.17.2952
RUN mkdir -p /app || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Sonarr/Sonarr/releases/download/v${VERSION}/Sonarr.main.${VERSION}.linux-x64.tar.gz" -o /tmp/Sonarr.tar.gz && \
    mkdir -p /app && \
    tar -xzf /tmp/Sonarr.tar.gz -C /app && rm -f /tmp/Sonarr.tar.gz && \
    chmod +x /app/Sonarr
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates curl icu-libs krb5-libs libgcc libstdc++ zlib 2>/dev/null && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /config /var/log/sonarr /var/cache/sonarr && chown -R 65532:65532 /config /var/log/sonarr /var/cache/sonarr 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /config

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8989"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
EXPOSE 8989

LABEL org.opencontainers.image.title="sonarr" \
      org.opencontainers.image.description="Sonarr - PVR for Usenet and BitTorrent users" \
      org.opencontainers.image.version="4.0.10" \
      org.opencontainers.image.vendor="Sonarr" \
      org.opencontainers.image.source="https://github.com/Sonarr/Sonarr" \
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
