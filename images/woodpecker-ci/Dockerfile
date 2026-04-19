# =============================================================================
# SOVEREIGN HARDENED WOODPECKER-CI
# Generated from template - Version: 2.0.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends woodpecker-server ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' woodpecker 2>/dev/null || true
RUN mkdir -p /app /var/log/woodpecker-server /var/cache/woodpecker-server && chown -R woodpecker:woodpecker /app /var/log/woodpecker-server /var/cache/woodpecker-server 2>/dev/null || true
USER woodpecker
WORKDIR /app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8000/healthz
ENTRYPOINT ["woodpecker-server"]
LABEL org.opencontainers.image.title="woodpecker-ci" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.vendor="Woodpecker" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
