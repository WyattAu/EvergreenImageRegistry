# =============================================================================
# SOVEREIGN HARDENED PHP
# Generated from template - Version: 8.3
# Constraint: debian-slim - PHP CLI runtime
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.3
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache \
    php-8.4 php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip
RUN adduser -u 65532 -D app 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php && chown -R app:app /app /var/log/php /var/cache/php 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="php" \
      org.opencontainers.image.version="8.3" \
      org.opencontainers.image.vendor="PHP" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM