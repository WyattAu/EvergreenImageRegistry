# =============================================================================
# SOVEREIGN HARDENED REDIS7
# Generated from template - Version: 7.4.1
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=7.4.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
# Create non-root user
RUN useradd -m -u 65532 -g '' redis 2>/dev/null || true
RUN mkdir -p /app /var/log/redis7 /var/cache/redis7 && chown -R redis:redis /app /var/log/redis7 /var/cache/redis7 2>/dev/null || true
USER redis:redis
WORKDIR /app
EXPOSE 6379
ENTRYPOINT ["redis"]
LABEL org.opencontainers.image.title="redis7" \
      org.opencontainers.image.version="7.4.1" \
      org.opencontainers.image.vendor="Redis" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM