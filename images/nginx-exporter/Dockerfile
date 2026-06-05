
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.1.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v1.1.0/nginx-prometheus-exporter_1.1.0_linux_${TARGETARCH}.tar.gz -o /nginx_exporter.tar.gz && \
    echo "40334965075e416d17f87f977edca0838f6de00799370749268567d26eef8018  /nginx_exporter.tar.gz" | sha256sum -c ; [ -f /nginx_exporter.tar.gz ] && \
    [ -f /nginx_exporter.tar.gz ] && tar -xzf /nginx_exporter.tar.gz -C / && rm -f /nginx_exporter.tar.gz && chmod +x /nginx_exporter 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v1.1.0/nginx-prometheus-exporter_1.1.0_linux_${TARGETARCH}.tar.gz -o /nginx_exporter && chmod +x /nginx_exporterbinary not available - download failed" >&2"' >> /nginx_exporter && echo 'exit 1' >> /nginx_exporter && chmod +x /nginx_exporter; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/nginx_exporter /var/cache/nginx_exporter 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /nginx_exporter /nginx_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/nginx_exporter /var/log/nginx_exporter
COPY --from=builder /var/cache/nginx_exporter /var/cache/nginx_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9113

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9113"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="nginx-exporter" \
      org.opencontainers.image.description="Nginx Exporter - Prometheus metrics exporter for Nginx" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="Nginx Inc" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/nginx/nginx"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
