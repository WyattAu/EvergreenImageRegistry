
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.70.5
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/netbirdio/netbird/releases/download/v0.29.1/netbird_${VERSION}_linux_${TARGETARCH}.tar.gz -o /netbird.tar.gz && \
    echo "4cfbaf0df70878a9e21add92e73da7719441d74f7151a2514a728b2c277dc288  /netbird.tar.gz" | sha256sum -c ; [ -f /netbird.tar.gz ] && \
    [ -f /netbird.tar.gz ] && tar -xzf /netbird.tar.gz -C / && rm -f /netbird.tar.gz && chmod +x /netbird 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/netbirdio/netbird/releases/download/v0.29.1/netbird_${VERSION}_linux_${TARGETARCH}.tar.gz -o /netbird && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/netbird /var/cache/netbird 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /netbird /netbird
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/netbird /var/log/netbird
COPY --from=builder /var/cache/netbird /var/cache/netbird
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 443 80

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:443"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="netbird" \
      org.opencontainers.image.description="netbird container image" \
      org.opencontainers.image.version="0.29.1" \
      org.opencontainers.image.vendor="NetBird" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/netbirdio/netbird"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
