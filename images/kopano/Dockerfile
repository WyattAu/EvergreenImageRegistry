# =============================================================================

# EVERGREEN HARDENED KOPANO

# Generated from template - Version: 12.1.0

# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable

# Priority: scratch > distroless > wolfi > debian-slim (last resort)

# =============================================================================

ARG VERSION=12.1.0
ARG TARGETARCH

ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache curl php-8.4 php-8.4-fpm php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip php-8.4-gd php-8.4-pdo_mysql php-8.4-mysqli php-8.4-pdo

RUN adduser -u 65532 -D www-data 2>/dev/null || true && \
    mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

WORKDIR /app

EXPOSE 80


HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]

LABEL org.opencontainers.image.title="kopano" \
      org.opencontainers.image.description="kopano container image" \
      org.opencontainers.image.version="12.1.0" \
      org.opencontainers.image.vendor="Kopano-dev/kopano-core" \
      org.opencontainers.image.source="https://github.com/Kopano-dev/kopano-core/releases" \
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

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
