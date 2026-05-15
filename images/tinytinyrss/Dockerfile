# =============================================================================

# EVERGREEN HARDENED TINYTINYRSS

# Generated from template - Version: 24.5

# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable

# Priority: scratch > distroless > wolfi > debian-slim (last resort)

# =============================================================================

ARG VERSION=24.5
ARG TARGETARCH

ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache curl php php-fpm php-curl php-mbstring php-xml php-zip php-pdo_mysql php-mysqli php-pgsql php-pdo_sqlite php-dom || true

RUN adduser -u 65532 -D www-data 2>/dev/null || true && \
    mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true

USER 65532:65532

WORKDIR /app

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:80/ || exit 1

ENTRYPOINT ["php"]

LABEL org.opencontainers.image.title="tinytinyrss" \
      org.opencontainers.image.description="tinytinyrss container image" \
      org.opencontainers.image.version="24.5" \
      org.opencontainers.image.vendor="tt-rss" \
      org.opencontainers.image.source="https://github.com/rr-/tt-rss/releases" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

STOPSIGNAL SIGTERM
