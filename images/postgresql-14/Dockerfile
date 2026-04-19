# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL-14
# Generated from template - Version: 14.13
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=14.13
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-14 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' postgres 2>/dev/null || true
RUN mkdir -p /app /var/log/postgres /var/cache/postgres && chown -R postgres:postgres /app /var/log/postgres /var/cache/postgres 2>/dev/null || true
USER postgres
WORKDIR /app
EXPOSE 5432
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD postgres pg_isready
ENTRYPOINT ["postgres"]
LABEL org.opencontainers.image.title="postgresql-14" \
      org.opencontainers.image.version="14.13" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
