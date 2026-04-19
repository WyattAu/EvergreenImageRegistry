# =============================================================================
# SOVEREIGN HARDENED REDIS7
# Generated from template - Version: 7.4.1
# =============================================================================

ARG VERSION=7.4.1
ARG BUILD_DATE

FROM alpine:7.4.1-alpine
RUN apk add --no-cache redis ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id redis 2>/dev/null || adduser -D -u 65534 redis
RUN mkdir -p /app /var/log/redis7 /var/cache/redis7 && chown -R redis:redis /app /var/log/redis7 /var/cache/redis7
USER redis:redis
WORKDIR /app
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD redis-cli ping
ENTRYPOINT ["redis-server"]
LABEL org.opencontainers.image.title="redis7" \
      org.opencontainers.image.version="7.4.1" \
      org.opencontainers.image.vendor="Redis" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
