# =============================================================================
# SOVEREIGN HARDENED LYCHEE
# Generated from template - Version: 4.17.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.17.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG GITHUB_TOKEN
RUN apk add --no-cache curl \
    php-8.4 php-8.4-fpm php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip php-8.4-gd php-8.4-pdo_mysql php-8.4-mysqli php-8.4-pdo_sqlite php-8.4-exif
RUN adduser -u 65532 -D www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="lychee" \
      org.opencontainers.image.version="4.17.0" \
      org.opencontainers.image.vendor="LycheeOrg/Lychee" \
      org.opencontainers.image.source="https://github.com/LycheeOrg/Lychee/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM