# =============================================================================

# EVERGREEN HARDENED TT-RSS

# Generated from template - Version: 24.5

# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable

# Priority: scratch > distroless > wolfi > debian-slim (last resort)

# =============================================================================

ARG VERSION=24.5
ARG TARGETARCH

ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache curl php-8.4 php-8.4-fpm php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip php-8.4-pdo_mysql php-8.4-mysqli php-8.4-pgsql php-8.4-pdo_sqlite php-8.4-dom

RUN adduser -u 65532 -D www-data 2>/dev/null || true && \
    mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true

USER 65532:65532

WORKDIR /app

EXPOSE 80


HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]

LABEL org.opencontainers.image.title="tt-rss" \
      org.opencontainers.image.description="tt-rss container image" \
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
