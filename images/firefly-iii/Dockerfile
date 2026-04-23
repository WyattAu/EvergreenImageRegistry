# =============================================================================
# SOVEREIGN HARDENED FIREFLY-III
# Generated from template - Version: 6.1.8
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=6.1.8
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache \
    php-8.4 php-8.4-fpm php-8.4-pdo_mysql php-8.4-mysqli php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip
RUN adduser -u 65532 -G '' -D www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true
USER www-data
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="firefly-iii" \
      org.opencontainers.image.version="6.1.8" \
      org.opencontainers.image.vendor="Firefly III" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM