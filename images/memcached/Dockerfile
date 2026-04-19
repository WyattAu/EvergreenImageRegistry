# =============================================================================
# SOVEREIGN HARDENED MEMCACHED
# Generated from template - Version: 1.6.26
# =============================================================================

ARG VERSION=1.6.26
ARG BUILD_DATE

FROM alpine:1.6.26-alpine
RUN apk add --no-cache memcached ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id memcached 2>/dev/null || adduser -D -u 65534 memcached
RUN mkdir -p /app /var/log/memcached /var/cache/memcached && chown -R memcached:memcached /app /var/log/memcached /var/cache/memcached
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
      sovereign.constraint.nonroot="true"
