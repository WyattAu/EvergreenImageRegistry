# =============================================================================
# SOVEREIGN HARDENED HEDGEDOC
# Generated from template - Version: 1.9.10
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.9.10
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends hedgedoc npm curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' hedgedoc 2>/dev/null || true
RUN mkdir -p /app /var/log/hedgedoc /var/cache/hedgedoc && chown -R hedgedoc:hedgedoc /app /var/log/hedgedoc /var/cache/hedgedoc 2>/dev/null || true
USER hedgedoc
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:3000/api/status
ENTRYPOINT ["hedgedoc"]
LABEL org.opencontainers.image.title="hedgedoc" \
      org.opencontainers.image.version="1.9.10" \
      org.opencontainers.image.vendor="HedgeDoc" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
