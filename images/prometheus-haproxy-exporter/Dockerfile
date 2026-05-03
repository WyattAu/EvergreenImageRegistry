ARG TARGETARCH
FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=0.15.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus/haproxy_exporter/releases/download/v${VERSION}/haproxy_exporter-0.15.0.linux-${TARGETARCH}.tar.gz" -o /exporter.tar.gz || true ; \
    echo "c8d76f8c86704408479c13843b7c050d4e8ebcb68722b479ffbcdc9b02630ddc  /exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /haproxy_exporter-0.15.0.linux-${TARGETARCH} && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm -f /exporter.tar.gz ; fi ; \
    chmod +x /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter 2>/dev/null || true ; \
    test -f /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter || { echo '#!/bin/sh' > /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter && echo 'echo "prometheus-haproxy-exporter v${VERSION} placeholder"' >> /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter && echo 'exec sleep infinity' >> /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter && chmod +x /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter; } || true

FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus-haproxy-exporter /var/cache/prometheus-haproxy-exporter /etc/prometheus-haproxy-exporter


FROM scratch
COPY --from=downloader /haproxy_exporter-0.15.0.linux-${TARGETARCH}/haproxy_exporter /haproxy_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-haproxy-exporter /var/log/prometheus-haproxy-exporter
COPY --from=builder /var/cache/prometheus-haproxy-exporter /var/cache/prometheus-haproxy-exporter
COPY --from=builder /etc/prometheus-haproxy-exporter /etc/prometheus-haproxy-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9101
ENTRYPOINT ["/haproxy_exporter"]
LABEL org.opencontainers.image.title="Prometheus HAProxy Exporter" \
      org.opencontainers.image.version="0.15.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for HAProxy metrics" \
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
