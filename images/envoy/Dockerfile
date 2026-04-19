# =============================================================================
# SOVEREIGN HARDENED ENVOY
# Generated from template - Version: 1.31.0
# =============================================================================

ARG VERSION=1.31.0
ARG BUILD_DATE

# Envoy requires complex build from source or official distribution
# Using official image with hardening applied
FROM envoyproxy/envoy:v1.31.0
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/envoy /var/cache/envoy && chown -R app:app /app /var/log/envoy /var/cache/envoy
USER app
WORKDIR /app
EXPOSE 80 443 9900
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -s http://localhost:80/ready || exit 1
ENTRYPOINT ["/usr/local/bin/envoy"]
LABEL org.opencontainers.image.title="envoy" \
      org.opencontainers.image.version="1.31.0" \
      org.opencontainers.image.vendor="Envoy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"