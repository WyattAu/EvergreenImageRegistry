
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION=2.10.5
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/grafana/tempo/releases/download/v${VERSION}/tempo_${VERSION}_linux_amd64.tar.gz -o /tempo.tar.gz && \
    [ -f /tempo.tar.gz ] && tar -xzf /tempo.tar.gz -C / && rm -f /tempo.tar.gz && chmod +x /tempo 2>/dev/null
FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/tempo /var/cache/tempo /var/tempo/wal 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /tempo /tempo
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tempo /var/log/tempo
COPY --from=builder /var/cache/tempo /var/cache/tempo
COPY --from=builder /var/tempo /var/tempo
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 3200

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3200"]

ENTRYPOINT ["/shim", "run", "-c", "/tempo"]
LABEL org.opencontainers.image.title="tempo" \
      org.opencontainers.image.description="Tempo - distributed tracing backend by Grafana" \
      org.opencontainers.image.version="2.10.5" \
      org.opencontainers.image.vendor="Grafana" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/grafana/tempo"

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
