# =============================================================================
# SOVEREIGN HARDENED TINYTINYRSS
# Generated from template - Version: 24.5
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=24.5
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache \
    php-8.4 php-8.4-fpm php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip php-8.4-pdo_mysql php-8.4-mysqli php-8.4-pgsql php-8.4-pdo_sqlite php-8.4-dom
RUN adduser -u 65532 -G '' -D www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="tinytinyrss" \
      org.opencontainers.image.version="24.5" \
      org.opencontainers.image.vendor="tt-rss" \
      org.opencontainers.image.source="https://github.com/rr-/tt-rss/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM