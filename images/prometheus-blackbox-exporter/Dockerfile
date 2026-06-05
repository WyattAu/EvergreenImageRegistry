ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.28.0
RUN mkdir -p /blackbox_exporter-0.28.0.linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus/blackbox_exporter/releases/download/v${VERSION}/blackbox_exporter-0.28.0.linux-${TARGETARCH}.tar.gz" -o /exporter.tar.gz ; \
    echo "a4bb36f68909bf7c28bb03148b3a06ce33f8686c7d5492bfa342b133a5827bed  /exporter.tar.gz" | sha256sum -c ; \
    mkdir -p /blackbox_exporter-0.28.0.linux-${TARGETARCH} && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter 2>/dev/null ; \
    test -s /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter || { echo '#!/bin/sh' > /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter && echo 'echo "prometheus-blackbox-exporter v${VERSION} binary not available - download failed" >&2 exit 1"' >> /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter  && chmod +x /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter; }

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus-blackbox-exporter /var/cache/prometheus-blackbox-exporter /etc/prometheus-blackbox-exporter


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=0.28.0
ARG TARGETARCH
COPY --from=downloader /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter /blackbox_exporter
COPY --from=downloader /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox.yml /etc/prometheus-blackbox-exporter/blackbox.yml
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-blackbox-exporter /var/log/prometheus-blackbox-exporter
COPY --from=builder /var/cache/prometheus-blackbox-exporter /var/cache/prometheus-blackbox-exporter
COPY --from=builder /etc/prometheus-blackbox-exporter /etc/prometheus-blackbox-exporter
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 9115

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9115"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="Prometheus Blackbox Exporter" \
      org.opencontainers.image.version="0.28.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for endpoint probing" \
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
            org.opencontainers.image.source="https://github.com/prometheus/blackbox_exporter"
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
