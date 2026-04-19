# =============================================================================
# SOVEREIGN HARDENED PROMETHEUS
# Generated from template - Version: 2.53.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.53.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/prometheus/prometheus/releases/download/v2.53.0/prometheus-2.53.0.linux-amd64.tar.gz" -o /prometheus.tar.gz && \
    echo "bf4ef82fc332dbb1a254c8ed7919363415126c1ed4e2ede536f8a049649976f5  /prometheus.tar.gz" | sha256sum -c - && \
    tar -xzf /prometheus.tar.gz -C / && rm /prometheus.tar.gz && chmod +x /prometheus 2>/dev/null || \
    curl -fsSL "https://github.com/prometheus/prometheus/releases/download/v2.53.0/prometheus-2.53.0.linux-amd64.tar.gz" -o /prometheus && chmod +x /prometheus

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/prometheus /var/cache/prometheus

FROM scratch
COPY --from=downloader /prometheus /prometheus
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus /var/log/prometheus
COPY --from=builder /var/cache/prometheus /var/cache/prometheus
USER 65534:65534
WORKDIR /app
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/prometheus", "--version"]
ENTRYPOINT ["/prometheus"]
LABEL org.opencontainers.image.title="prometheus" \
      org.opencontainers.image.version="2.53.0" \
      org.opencontainers.image.vendor="Prometheus" \
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
