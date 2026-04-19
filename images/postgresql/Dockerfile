# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL
# Generated from template - Version: 17.4
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=17.4
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends postgresql17 postgresql17-client ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' postgres 2>/dev/null || true
RUN mkdir -p /app /var/log/postgresql /var/cache/postgresql && chown -R postgres:postgres /app /var/log/postgresql /var/cache/postgresql 2>/dev/null || true
USER postgres:postgres
WORKDIR /app
EXPOSE 5432
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pg_isready
ENTRYPOINT ["postgres"]
LABEL org.opencontainers.image.title="postgresql" \
      org.opencontainers.image.version="17.4" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
