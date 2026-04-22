# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS X509 CERTIFICATE EXPORTER
# Version: 3.9.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=3.9.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/enix/x509-certificate-exporter/releases/download/v${VERSION}/x509-certificate-exporter-${VERSION}-linux-amd64.tar.gz" -o /x509-exporter.tar.gz && \
    tar -xzf /x509-exporter.tar.gz -C / && rm /x509-exporter.tar.gz && chmod +x /x509-certificate-exporter

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/x509_exporter /var/cache/x509_exporter

FROM scratch
COPY --from=downloader /x509-certificate-exporter /x509-certificate-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/x509_exporter /var/log/x509_exporter
COPY --from=builder /var/cache/x509_exporter /var/cache/x509_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9793
ENTRYPOINT ["/x509-certificate-exporter"]
LABEL org.opencontainers.image.title="prometheus-x509-exporter" \
      org.opencontainers.image.version="3.9.0" \
      org.opencontainers.image.vendor="Enix" \
      org.opencontainers.image.description="Prometheus exporter for X.509 certificate expiry metrics" \
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