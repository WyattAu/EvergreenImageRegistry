# =============================================================================
# SOVEREIGN HARDENED MEMCACHED
# Generated from template - Version: 1.6.26
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=1.6.26
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends memcached ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' memcached 2>/dev/null || true
RUN mkdir -p /app /var/log/memcached /var/cache/memcached && chown -R memcached:memcached /app /var/log/memcached /var/cache/memcached 2>/dev/null || true
USER memcached:memcached
WORKDIR /app
EXPOSE 11211
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD stats
ENTRYPOINT ["memcached"]
LABEL org.opencontainers.image.title="memcached" \
      org.opencontainers.image.version="1.6.26" \
      org.opencontainers.image.vendor="Memcached" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
