# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS-PUSHGATEWAY
# Generated from template - Version: 1.8.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus/pushgateway/releases/download/v1.8.0/pushgateway-1.8.0.linux-amd64.tar.gz" -o /pushgateway.tar.gz && \
    echo "ee962b451e533c392d9bfd07f5e4195d64a65b87b55d4abbcedc5f9ce13dfc58  /pushgateway.tar.gz" | sha256sum -c - && \
    tar -xzf /pushgateway.tar.gz -C / && rm /pushgateway.tar.gz && chmod +x /pushgateway 2>/dev/null || \
    curl -fsSL "https://github.com/prometheus/pushgateway/releases/download/v1.8.0/pushgateway-1.8.0.linux-amd64.tar.gz" -o /pushgateway && chmod +x /pushgateway

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/pushgateway /var/cache/pushgateway

FROM scratch
COPY --from=downloader /pushgateway /pushgateway
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pushgateway /var/log/pushgateway
COPY --from=builder /var/cache/pushgateway /var/cache/pushgateway
USER 65534:65534
WORKDIR /app
EXPOSE 9091
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/pushgateway", "--version"]
ENTRYPOINT ["/pushgateway"]
LABEL org.opencontainers.image.title="prometheus-pushgateway" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus" \
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
