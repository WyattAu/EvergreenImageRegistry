# =============================================================================
# SOVEREIGN HARDENED SNMP EXPORTER (standalone)
# Version: 0.26.0
# Constraint: scratch - purest form, no shell, no package manager
# NOTE: Separate from prometheus-snmp-exporter (v0.27.0) - uses different
#       version to avoid full duplication, targets standalone SNMP deployments
# =============================================================================

ARG VERSION=0.26.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus/snmp_exporter/releases/download/v${VERSION}/snmp_exporter-${VERSION}.linux-amd64.tar.gz" -o /snmp_exporter.tar.gz && \
    tar -xzf /snmp_exporter.tar.gz -C / && rm /snmp_exporter.tar.gz && chmod +x /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/snmp_exporter /var/cache/snmp_exporter /etc/snmp_exporter

FROM scratch
COPY --from=downloader /snmp_exporter-${VERSION}.linux-amd64/snmp_exporter /snmp_exporter
COPY --from=downloader /snmp_exporter-${VERSION}.linux-amd64/snmp.yml /etc/snmp_exporter/snmp.yml
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/snmp_exporter /var/log/snmp_exporter
COPY --from=builder /var/cache/snmp_exporter /var/cache/snmp_exporter
COPY --from=builder /etc/snmp_exporter /etc/snmp_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9116
ENTRYPOINT ["/snmp_exporter"]
LABEL org.opencontainers.image.title="snmp-exporter" \
      org.opencontainers.image.version="0.26.0" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Standalone Prometheus SNMP exporter (v0.26.0, separate from prometheus-snmp-exporter)" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM