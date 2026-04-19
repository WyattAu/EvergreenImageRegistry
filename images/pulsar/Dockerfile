# =============================================================================
# SOVEREIGN HARDENED PULSAR
# Generated from template - Version: 3.3.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends pulsar ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' pulsar 2>/dev/null || true
RUN mkdir -p /app /var/log/pulsar /var/cache/pulsar && chown -R pulsar:pulsar /app /var/log/pulsar /var/cache/pulsar 2>/dev/null || true
USER pulsar
WORKDIR /app
EXPOSE 6650 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pulsar curl -s localhost:8080/admin/v2/persistent/public/sample/ready
ENTRYPOINT ["pulsar"]
LABEL org.opencontainers.image.title="pulsar" \
      org.opencontainers.image.version="3.3.0" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
