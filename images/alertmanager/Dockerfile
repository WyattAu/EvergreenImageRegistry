ARG TARGETARCH
ARG VERSION=v0.32.1
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION=v0.32.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus/alertmanager/releases/download/${VERSION}/alertmanager-0.32.1.linux-amd64.tar.gz" -o /alertmanager.tar.gz && \
    tar -xzf /alertmanager.tar.gz -C /tmp && \
    cp /tmp/alertmanager-0.32.1.linux-amd64/alertmanager /alertmanager && \
    chmod +x /alertmanager && \
    mkdir -p /alertmanager-data && chown -R 65532:65532 /alertmanager-data

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=downloader /alertmanager /alertmanager
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /alertmanager-data /alertmanager-data
USER ${APP_UID}:${APP_GID}
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /
EXPOSE 9093 9101
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9093"]
ENTRYPOINT ["/shim", "run", "-c", "/alertmanager"]
LABEL org.opencontainers.image.title="alertmanager" \
      org.opencontainers.image.description="Prometheus Alertmanager" \
      org.opencontainers.image.version="v0.32.1" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://github.com/prometheus/alertmanager" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch" \
      evergreen.build.type="binary-download" \
      evergreen.metrics.native="ztunnel" \
      evergreen.health.type="http" \
      evergreen.health.endpoint="/livez" \
      evergreen.health.listen="0.0.0.0:9101" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
# cache bust 1781029690
# trigger build
# trigger build
