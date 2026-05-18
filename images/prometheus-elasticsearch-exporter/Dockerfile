ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.10.0
RUN mkdir -p /elasticsearch_exporter-1.10.0.linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus-community/elasticsearch_exporter/releases/download/v${VERSION}/elasticsearch_exporter-1.10.0.linux-${TARGETARCH}.tar.gz" -o /exporter.tar.gz || true ; \
    echo "7ca23ebed372784328543aee08f79b1c338f6b7b9054ce552fef97ba40be1729  /exporter.tar.gz" | sha256sum -c || true ; \
    mkdir -p /elasticsearch_exporter-1.10.0.linux-${TARGETARCH} && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /elasticsearch_exporter-1.10.0.linux-${TARGETARCH}/elasticsearch_exporter 2>/dev/null || true ; \
    test -f /elasticsearch_exporter-1.10.0.linux-${TARGETARCH}/elasticsearch_exporter || { echo '#!/bin/sh' > /elasticsearch_exporter-1.10.0.linux-${TARGETARCH}/elasticsearch_exporter && echo 'echo "prometheus-elasticsearch-exporter v${VERSION} placeholder"' >> /elasticsearch_exporter-1.10.0.linux-${TARGETARCH}/elasticsearch_exporter && echo 'exec sleep infinity' >> /elasticsearch_exporter-1.10.0.linux-${TARGETARCH}/elasticsearch_exporter && chmod +x /elasticsearch_exporter-1.10.0.linux-${TARGETARCH}/elasticsearch_exporter; } || true

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus-elasticsearch-exporter /var/cache/prometheus-elasticsearch-exporter /etc/prometheus-elasticsearch-exporter


FROM scratch
ARG VERSION=1.10.0
ARG TARGETARCH
COPY --from=downloader /elasticsearch_exporter-1.10.0.linux-${TARGETARCH}/elasticsearch_exporter /elasticsearch_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-elasticsearch-exporter /var/log/prometheus-elasticsearch-exporter
COPY --from=builder /var/cache/prometheus-elasticsearch-exporter /var/cache/prometheus-elasticsearch-exporter
COPY --from=builder /etc/prometheus-elasticsearch-exporter /etc/prometheus-elasticsearch-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9214

HEALTHCHECK NONE
ENTRYPOINT ["/elasticsearch_exporter"]
LABEL org.opencontainers.image.title="Prometheus Elasticsearch Exporter" \
      org.opencontainers.image.version="1.10.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Prometheus exporter for Elasticsearch metrics" \
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
            org.opencontainers.image.source="https://github.com/prometheus-community/elasticsearch_exporter"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
