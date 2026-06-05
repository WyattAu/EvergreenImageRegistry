ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.13.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/memcached_exporter/releases/download/v0.13.0/memcached_exporter-0.13.0.linux-${TARGETARCH}.tar.gz -o /memcached_exporter.tar.gz && \
    echo "4be294cbddf93ba1ca56f39f259a718148353a74096de5c06237a488e121356f  /memcached_exporter.tar.gz" | sha256sum -c ; [ -f /memcached_exporter.tar.gz ] && \
    [ -f /memcached_exporter.tar.gz ] && tar -xzf /memcached_exporter.tar.gz -C / && rm -f /memcached_exporter.tar.gz && chmod +x /memcached_exporter 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/memcached_exporter/releases/download/v0.13.0/memcached_exporter-0.13.0.linux-${TARGETARCH}.tar.gz -o /memcached_exporter && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/memcached_exporter /var/cache/memcached_exporter 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /memcached_exporter /memcached_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/memcached_exporter /var/log/memcached_exporter
COPY --from=builder /var/cache/memcached_exporter /var/cache/memcached_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9150

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9150"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="memcached-exporter" \
      org.opencontainers.image.description="memcached-exporter container image" \
      org.opencontainers.image.version="0.13.0" \
      org.opencontainers.image.vendor="Prometheus" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/prometheus/memcached_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
