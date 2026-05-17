ARG VERSION=8.3.2
ARG TARGETARCH
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /etc/nginx/nginx.conf || true
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true && \
    apt-get update && apt-get install -y --no-install-recommends \
        php-fpm php8.4 php-curl php-gd php-mbstring php-xml zip php-intl php-mysql openssl php-pdo json-c \
        nginx ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx ; \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache php-fpm php php-curl php-gd php-mbstring php-xml zip php-intl php-pdo_mysql php-mysqli openssl php-pdo json-c nginx ca-certificates || true && \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php 2>/dev/null || true
COPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:80/ || exit 1
ENTRYPOINT ["php-fpm8.4"]
LABEL org.opencontainers.image.title="espocrm" \
      org.opencontainers.image.description="espocrm container image" \
      org.opencontainers.image.version="8.3.2" \
      org.opencontainers.image.vendor="EspoCRM" \
      org.opencontainers.image.source="https://github.com/espocrm/espocrm" \
      evergreen.image.tier="2" \
      evergreen.image.category="crm-erp" \
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
STOPSIGNAL SIGTERM
