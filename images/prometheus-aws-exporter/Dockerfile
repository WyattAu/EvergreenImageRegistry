# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS AWS (YACE) EXPORTER
# Version: 0.55.0
# Constraint: scratch - purest form, no shell, no package manager
# =============================================================================

ARG VERSION=0.55.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus-community/yet-another-cloudwatch-exporter/releases/download/v${VERSION}/yace-${VERSION}-linux-amd64.tar.gz" -o /yace.tar.gz && \
    tar -xzf /yace.tar.gz -C / && rm /yace.tar.gz && chmod +x /yace-${VERSION}-linux-amd64

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/yace /var/cache/yace /etc/yace

FROM scratch
COPY --from=downloader /yace-${VERSION}-linux-amd64 /yace
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/yace /var/log/yace
COPY --from=builder /var/cache/yace /var/cache/yace
COPY --from=builder /etc/yace /etc/yace
USER 65534:65534
WORKDIR /app
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/yace", "--version"]
ENTRYPOINT ["/yace"]
LABEL org.opencontainers.image.title="prometheus-aws-exporter" \
      org.opencontainers.image.version="0.55.0" \
      org.opencontainers.image.vendor="Prometheus Community" \
      org.opencontainers.image.description="Yet Another CloudWatch Exporter (YACE) for AWS metrics" \
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
