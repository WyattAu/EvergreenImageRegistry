ARG VERSION=v0.16.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM prom/cloudwatch-exporter:v0.16.0@sha256:fca3c9df0b737ce3509f7361017bcd61b62cfc4f5667ae3d99270310c40795c5 AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /var/log/prometheus-cloudwatch-exporter /var/cache/prometheus-cloudwatch-exporter 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=upstream /bin/cloudwatch_exporter /cloudwatch_exporter
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-cloudwatch-exporter /var/log/prometheus-cloudwatch-exporter
COPY --from=builder /var/cache/prometheus-cloudwatch-exporter /var/cache/prometheus-cloudwatch-exporter

WORKDIR /app

EXPOSE 9106
EXPOSE 9101

LABEL org.opencontainers.image.title="prometheus-cloudwatch-exporter" org.opencontainers.image.version="0.15.0" org.opencontainers.image.vendor="Prometheus Community" org.opencontainers.image.description="Prometheus exporter for AWS CloudWatch metrics" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" evergreen.hft.cpu-pins="4-5" evergreen.hft.cpu-pins-mode="exclusive" evergreen.hft.deploy-strategy="hft-stateful" evergreen.hft.pre-stop-hook="true" evergreen.hft.pre-stop-delay="5s" evergreen.hft.connection-drain="true" evergreen.hft.sched-policy="SCHED_OTHER" \
      org.opencontainers.image.source="https://github.com/prometheus/cloudwatch_exporter"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9106"]

ENTRYPOINT ["/shim", "run", "-c", "/bin/cloudwatch-exporter"]
