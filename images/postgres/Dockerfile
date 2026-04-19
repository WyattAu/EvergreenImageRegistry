# =============================================================================
# SOVEREIGN HARDENED POSTGRES
# Generated from template - Version: 17.4
# =============================================================================

ARG VERSION=17.4
ARG BUILD_DATE

FROM postgres:17.4
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
RUN mkdir -p /app /var/log/postgres /var/cache/postgres && chown -R app:app /app /var/log/postgres /var/cache/postgres
USER app
WORKDIR /app
EXPOSE 5432
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pg_isready -U postgres -h localhost
ENTRYPOINT ["postgres"]
LABEL org.opencontainers.image.title="postgres" \
      org.opencontainers.image.version="17.4" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"