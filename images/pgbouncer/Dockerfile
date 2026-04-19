# =============================================================================
# SOVEREIGN HARDENED PGBOUNCER
# Generated from template - Version: 1.22.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.22.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends pgbouncer ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' pgbouncer 2>/dev/null || true
RUN mkdir -p /app /var/log/pgbouncer /var/cache/pgbouncer && chown -R pgbouncer:pgbouncer /app /var/log/pgbouncer /var/cache/pgbouncer 2>/dev/null || true
USER pgbouncer
WORKDIR /app
EXPOSE 6432
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pgbouncer pgbouncer --version
ENTRYPOINT ["pgbouncer"]
LABEL org.opencontainers.image.title="pgbouncer" \
      org.opencontainers.image.version="1.22.1" \
      org.opencontainers.image.vendor="PgBouncer" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
