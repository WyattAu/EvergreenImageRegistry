ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v1.83.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/oliver006/redis_exporter/releases/download/v1.68.0/redis_exporter-v1.68.0.linux-${TARGETARCH}.tar.gz -o /redis_exporter.tar.gz && \
    # TODO: update sha256 for new version
    echo "870ca02b568e4df6bbf24555611d6ca98c673071668334f230abeb2fb52c59e3  /redis_exporter.tar.gz" | sha256sum -c ; [ -f /redis_exporter.tar.gz ] && \
    [ -f /redis_exporter.tar.gz ] && tar -xzf /redis_exporter.tar.gz -C / && rm -f /redis_exporter.tar.gz && chmod +x /redis_exporter 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/oliver006/redis_exporter/releases/download/v1.68.0/redis_exporter-v1.68.0.linux-${TARGETARCH}.tar.gz -o /redis_exporter && { echo "Binary not available - download failed" >&2; exit 1; }
    mkdir -p /app /var/log/redis_exporter /var/cache/redis_exporter 2>/dev/null || true

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /redis_exporter /redis_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /app /app
COPY --from=downloader /var/log/redis_exporter /var/log/redis_exporter
COPY --from=downloader /var/cache/redis_exporter /var/cache/redis_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9121

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9121"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="redis-exporter" \
      org.opencontainers.image.description="Redis Exporter - Prometheus exporter for Redis" \
      org.opencontainers.image.version="v1.83.0" \
      org.opencontainers.image.vendor="Prometheus" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/oliver006/redis_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
