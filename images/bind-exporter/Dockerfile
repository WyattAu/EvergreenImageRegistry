ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.7.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus-community/bind_exporter/releases/download/v0.7.0/bind_exporter-0.7.0.linux-${TARGETARCH}.tar.gz -o /bind_exporter.tar.gz && \
    echo "cc316fc3f8df6515bc4347faa5e44d01c74016df09a3ce1a49de99328767646b  /bind_exporter.tar.gz" | sha256sum -c ; [ -f /bind_exporter.tar.gz ] && \
    [ -f /bind_exporter.tar.gz ] && tar -xzf /bind_exporter.tar.gz -C / && rm -f /bind_exporter.tar.gz && chmod +x /bind_exporter 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus-community/bind_exporter/releases/download/v0.7.0/bind_exporter-0.7.0.linux-${TARGETARCH}.tar.gz -o /bind_exporter && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/bind_exporter /var/cache/bind_exporter 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /bind_exporter /bind_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/bind_exporter /var/log/bind_exporter
COPY --from=builder /var/cache/bind_exporter /var/cache/bind_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9119

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9119"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="bind-exporter" \
      org.opencontainers.image.description="bind-exporter container image" \
      org.opencontainers.image.version="0.7.0" \
      org.opencontainers.image.vendor="Prometheus" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/prometheus/bind_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
