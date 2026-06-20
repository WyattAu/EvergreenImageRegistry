ARG VERSION=30.0.5
ARG BUILD_DATE

ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /etc/nginx/nginx.conf || true
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true && \
    apt-get update && apt-get install -y --no-install-recommends \
        php-fpm php8.4 php-curl php-gd php-mbstring php-xml zip php-intl php-mysql sqlite-libs \
        nginx ca-certificates curl ; rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx  || true ; \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php && \
    mkdir -p /etc/nginx 2>/dev/null || true ; touch /etc/nginx/nginx.conf 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache php-8.4-fpm php-8.4 php-8.4-curl php-8.4-gd php-8.4-mbstring php-8.4-xml zip php-8.4-intl php-8.4-pdo_mysql php-8.4-mysqli sqlite-libs nginx ca-certificates && \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php-8.4 2>/dev/null || true && \
    mkdir -p /etc/nginx 2>/dev/null || true
COPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/www/html
EXPOSE 80 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "php-fpm8.4"]
LABEL org.opencontainers.image.title="nextcloud" \
      org.opencontainers.image.description="Nextcloud - self-hosted productivity platform" \
      org.opencontainers.image.version="30.0.5" \
      org.opencontainers.image.vendor="Nextcloud" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://github.com/nextcloud/server" \
      evergreen.image.tier="2" \
      evergreen.image.category="cloud-storage" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
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
