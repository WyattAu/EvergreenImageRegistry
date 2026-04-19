# =============================================================================
# SOVEREIGN HARDENED REDIS
# Generated from template - Version: 7.4.1
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=7.4.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:7.4.1
RUN apk add --no-cache redis ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 redis 2>/dev/null || true
RUN mkdir -p /app /var/log/redis /var/cache/redis && chown -R redis:redis /app /var/log/redis /var/cache/redis 2>/dev/null || true
USER redis:redis
WORKDIR /app
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD redis-cli ping
ENTRYPOINT ["redis-server"]
LABEL org.opencontainers.image.title="redis" \
      org.opencontainers.image.version="7.4.1" \
      org.opencontainers.image.vendor="Redis" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
