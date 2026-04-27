ARG VERSION=8.2.5
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true

RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.4-fpm php8.4 php8.4-curl php8.4-gd php8.4-mbstring php8.4-xml zip php8.4-intl php8.4-mysql sqlite-libs json-c \
        nginx ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true

RUN mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx  || true \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php 2>/dev/null || true
RUN mkdir -p /etc/nginx 2>/dev/null || true ; touch /etc/nginx/nginx.conf 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache php-8.4-fpm php-8.4 php-8.4-curl php-8.4-gd php-8.4-mbstring php-8.4-xml zip php-8.4-intl php-8.4-pdo_mysql php-8.4-mysqli sqlite-libs json-c nginx ca-certificates 
RUN chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php 2>/dev/null || true
RUN mkdir -p /etc/nginx 2>/dev/null || true
COPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf
    RUN chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php
COPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80 443
ENTRYPOINT ["php-fpm8.4"]
LABEL org.opencontainers.image.title="pydio" \
      org.opencontainers.image.version="8.2.5" \
      org.opencontainers.image.vendor="Pydio" \
      org.opencontainers.image.source="https://github.com/pydio/pydio-core" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM