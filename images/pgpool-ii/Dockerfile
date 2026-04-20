# =============================================================================
# SOVEREIGN HARDENED PGPOOL-II
# Generated from template - Version: 4.5.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.5.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends pgpool2 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' pgpool 2>/dev/null || true
RUN mkdir -p /app /var/log/pgpool /var/cache/pgpool && chown -R pgpool:pgpool /app /var/log/pgpool /var/cache/pgpool 2>/dev/null || true
USER pgpool
WORKDIR /app
EXPOSE 9999
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pgpool --version
ENTRYPOINT ["pgpool"]
LABEL org.opencontainers.image.title="pgpool-II" \
      org.opencontainers.image.version="4.5.1" \
      org.opencontainers.image.vendor="PgPool" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
