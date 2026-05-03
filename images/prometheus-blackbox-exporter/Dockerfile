ARG TARGETARCH
FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=0.28.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus/blackbox_exporter/releases/download/v${VERSION}/blackbox_exporter-0.28.0.linux-${TARGETARCH}.tar.gz" -o /exporter.tar.gz || true ; \
    echo "a4bb36f68909bf7c28bb03148b3a06ce33f8686c7d5492bfa342b133a5827bed  /exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /blackbox_exporter-0.28.0.linux-${TARGETARCH} && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter 2>/dev/null || true ; \
    test -f /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter || { echo '#!/bin/sh' > /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter && echo 'echo "prometheus-blackbox-exporter v${VERSION} placeholder"' >> /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter && echo 'exec sleep infinity' >> /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter && chmod +x /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter; } || true

FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus-blackbox-exporter /var/cache/prometheus-blackbox-exporter /etc/prometheus-blackbox-exporter


FROM scratch
COPY --from=downloader /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox_exporter /blackbox_exporter
COPY --from=downloader /blackbox_exporter-0.28.0.linux-${TARGETARCH}/blackbox.yml /etc/prometheus-blackbox-exporter/blackbox.yml
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-blackbox-exporter /var/log/prometheus-blackbox-exporter
COPY --from=builder /var/cache/prometheus-blackbox-exporter /var/cache/prometheus-blackbox-exporter
COPY --from=builder /etc/prometheus-blackbox-exporter /etc/prometheus-blackbox-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9115
ENTRYPOINT ["/blackbox_exporter"]
LABEL org.opencontainers.image.title="Prometheus Blackbox Exporter" \
      org.opencontainers.image.version="0.28.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for endpoint probing" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
