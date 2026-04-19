# =============================================================================
# SOVEREIGN HARDENED KUBE-STATE-METRICS
# Generated from template - Version: 2.12.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.12.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/kubernetes/kube-state-metrics/releases/download/v2.12.0/kube-state-metrics-2.12.0.linux-amd64.tar.gz" -o /kube-state-metrics.tar.gz && \
    tar -xzf /kube-state-metrics.tar.gz -C / && rm /kube-state-metrics.tar.gz && chmod +x /kube-state-metrics 2>/dev/null || \
    curl -fsSL "https://github.com/kubernetes/kube-state-metrics/releases/download/v2.12.0/kube-state-metrics-2.12.0.linux-amd64.tar.gz" -o /kube-state-metrics && chmod +x /kube-state-metrics

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kube-state-metrics /var/cache/kube-state-metrics

FROM scratch
COPY --from=downloader /kube-state-metrics /kube-state-metrics
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-state-metrics /var/log/kube-state-metrics
COPY --from=builder /var/cache/kube-state-metrics /var/cache/kube-state-metrics
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD kube-state-metrics kube-state-metrics --version
ENTRYPOINT ["/kube-state-metrics"]
LABEL org.opencontainers.image.title="kube-state-metrics" \
      org.opencontainers.image.version="2.12.0" \
      org.opencontainers.image.vendor="Kubernetes" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
