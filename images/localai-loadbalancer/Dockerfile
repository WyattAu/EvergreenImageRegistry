# =============================================================================
# SOVEREIGN HARDENED LOCALAI-LOADBALANCER
# Generated from template - Version: 2.30.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.30.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mudler/LocalAI/releases/download/v2.30.0/localai-loadbalancer-linux-amd64" -o /localai-loadbalancer.tar.gz && \
    tar -xzf /localai-loadbalancer.tar.gz -C / && rm /localai-loadbalancer.tar.gz && chmod +x /localai-loadbalancer 2>/dev/null || \
    curl -fsSL "https://github.com/mudler/LocalAI/releases/download/v2.30.0/localai-loadbalancer-linux-amd64" -o /localai-loadbalancer && chmod +x /localai-loadbalancer

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/localai-loadbalancer /var/cache/localai-loadbalancer

FROM scratch
COPY --from=downloader /localai-loadbalancer /localai-loadbalancer
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/localai-loadbalancer /var/log/localai-loadbalancer
COPY --from=builder /var/cache/localai-loadbalancer /var/cache/localai-loadbalancer
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/localai-loadbalancer", "--version"]
ENTRYPOINT ["/localai-loadbalancer"]
LABEL org.opencontainers.image.title="localai-loadbalancer" \
      org.opencontainers.image.version="2.30.0" \
      org.opencontainers.image.vendor="mudler/LocalAI" \
      org.opencontainers.image.source="https://github.com/mudler/LocalAI/releases/download/v2.30.0" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
