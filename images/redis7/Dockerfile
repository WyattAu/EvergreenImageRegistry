# =============================================================================
# EVERGREEN HARDENED REDIS7
# Generated from template - Version: 7.4.1
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=7.4.1
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates 
# Create non-root user
RUN adduser -u 65532 -D redis 2>/dev/null || true
RUN mkdir -p /app /var/log/redis7 /var/cache/redis7 && chown -R redis:redis /app /var/log/redis7 /var/cache/redis7 2>/dev/null || true
USER redis:redis
WORKDIR /app
EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD redis-cli ping
ENTRYPOINT ["redis"]
LABEL org.opencontainers.image.title="redis7" \
      org.opencontainers.image.version="7.4.1" \
      org.opencontainers.image.vendor="Redis" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
