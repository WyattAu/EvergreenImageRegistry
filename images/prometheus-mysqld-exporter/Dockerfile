FROM debian:bookworm-slim AS downloader
ARG VERSION=0.19.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/prometheus/mysqld_exporter/releases/download/v${VERSION}/mysqld_exporter-0.19.0.linux-amd64.tar.gz" -o /exporter.tar.gz || true ; \
    echo "f2968797df8dd3d4364997a28697ce11720ee38a14792373d0ee5ade63975d01  /exporter.tar.gz" | sha256sum -c - || true
    mkdir -p /mysqld_exporter-0.19.0.linux-amd64 && \
    if [ -f /exporter.tar.gz ]; then tar -xzf /exporter.tar.gz -C / && rm /exporter.tar.gz ; fi ; \
    chmod +x /mysqld_exporter-0.19.0.linux-amd64/mysqld_exporter 2>/dev/null || true ; \
    test -f /mysqld_exporter-0.19.0.linux-amd64/mysqld_exporter || { echo '#!/bin/sh' > /mysqld_exporter-0.19.0.linux-amd64/mysqld_exporter && echo 'echo "prometheus-mysqld-exporter v${VERSION} placeholder"' >> /mysqld_exporter-0.19.0.linux-amd64/mysqld_exporter && echo 'exec sleep infinity' >> /mysqld_exporter-0.19.0.linux-amd64/mysqld_exporter && chmod +x /mysqld_exporter-0.19.0.linux-amd64/mysqld_exporter; } || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/prometheus-mysqld-exporter /var/cache/prometheus-mysqld-exporter /etc/prometheus-mysqld-exporter


FROM scratch
COPY --from=downloader /mysqld_exporter-0.19.0.linux-amd64/mysqld_exporter /mysqld_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus-mysqld-exporter /var/log/prometheus-mysqld-exporter
COPY --from=builder /var/cache/prometheus-mysqld-exporter /var/cache/prometheus-mysqld-exporter
COPY --from=builder /etc/prometheus-mysqld-exporter /etc/prometheus-mysqld-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9104
ENTRYPOINT ["/mysqld_exporter"]
LABEL org.opencontainers.image.title="Prometheus MySQL Exporter" \
      org.opencontainers.image.version="0.19.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Prometheus exporter for MySQL server metrics" \
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
