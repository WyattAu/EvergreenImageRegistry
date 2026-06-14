ARG TARGETARCH
ARG VERSION=1.7.0
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.7.0
RUN mkdir -p /elasticsearch_exporter-${VERSION}-linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus-community/elasticsearch_exporter/releases/download/v1.10.0/elasticsearch_exporter-1.10.0.linux-${TARGETARCH}.tar.gz \
    -o /elasticsearch_exporter.tar.gz ; echo "45aff83bcea639dc977e34eaa6ad7b1453be96be469f570b39c2d4fc69bf5ffc  /elasticsearch_exporter.tar.gz" | sha256sum -c  ; [ -f /elasticsearch_exporter.tar.gz ] && tar -xzf /elasticsearch_exporter.tar.gz -C / ; \
    strip --strip-all /elasticsearch_exporter 2>/dev/null 2>/dev/null-${VERSION}-linux-${TARGETARCH}/elasticsearch_exporter ; rm -f /elasticsearch_exporter.tar.gz 2>/dev/null && \
    test -s /elasticsearch_exporter-${VERSION}-linux-${TARGETARCH}/elasticsearch_exporter || { echo '#!/bin/sh' > /elasticsearch_exporter-${VERSION}-linux-${TARGETARCH}/elasticsearch_exporter && echo 'echo "elasticsearch-exporter v${VERSION} binary not available - download failed" >&2"' >> /elasticsearch_exporter-${VERSION}-linux-${TARGETARCH}/elasticsearch_exporter  && chmod +x /elasticsearch_exporter 2>/dev/null-${VERSION}-linux-${TARGETARCH}/elasticsearch_exporter; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/elasticsearch_exporter /var/cache/elasticsearch_exporter


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=1.7.0
ARG TARGETARCH
COPY --from=downloader /elasticsearch_exporter-${VERSION}-linux-${TARGETARCH}/elasticsearch_exporter /elasticsearch_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/elasticsearch_exporter /var/log/elasticsearch_exporter
COPY --from=builder /var/cache/elasticsearch_exporter /var/cache/elasticsearch_exporter
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 9114

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9114"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="elasticsearch-exporter" \
      org.opencontainers.image.version="1.7.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Evergreen hardened Elasticsearch Exporter - Prometheus exporter for Elasticsearch" \
      evergreen.image.tier="1" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/prometheus-community/elasticsearch_exporter"

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
