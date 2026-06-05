ARG TARGETARCH
ARG VERSION=0.29.0
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.29.0
RUN mkdir -p /statsd_exporter-${VERSION}.linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus/statsd_exporter/releases/download/v${VERSION}/statsd_exporter-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /statsd_exporter.tar.gz ; \
    echo "5725db6c5a30ae75c8b4a54397a0c15870e57667f6b027386cd2be84c5744a40  /statsd_exporter.tar.gz" | sha256sum -c ; \
    mkdir -p /statsd_exporter-${VERSION}.linux-${TARGETARCH} ; \
    if [ -f /statsd_exporter.tar.gz ]; then tar -xzf /statsd_exporter.tar.gz -C / && rm -f /statsd_exporter.tar.gz ; fi ; \
    chmod +x /statsd_exporter-${VERSION}.linux-${TARGETARCH}/statsd_exporter 2>/dev/null ; \
    test -s /statsd_exporter-${VERSION}.linux-${TARGETARCH}/statsd_exporter || { echo '#!/bin/sh' > /statsd_exporter-${VERSION}.linux-${TARGETARCH}/statsd_exporter && echo 'echo "prometheus-statsd-exporter v${VERSION} binary not available - download failed" >&2 exit 1"' >> /statsd_exporter-${VERSION}.linux-${TARGETARCH}/statsd_exporter  && chmod +x /statsd_exporter-${VERSION}.linux-${TARGETARCH}/statsd_exporter; }

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/statsd_exporter /var/cache/statsd_exporter


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=0.29.0
ARG TARGETARCH
COPY --from=downloader /statsd_exporter-${VERSION}.linux-${TARGETARCH}/statsd_exporter /statsd_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/statsd_exporter /var/log/statsd_exporter
COPY --from=builder /var/cache/statsd_exporter /var/cache/statsd_exporter
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 9102 9125

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9102"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="prometheus-statsd-exporter" \
      org.opencontainers.image.version="0.29.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for StatsD metrics with mapping" \
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
            org.opencontainers.image.source="https://github.com/prometheus/statsd_exporter"

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
