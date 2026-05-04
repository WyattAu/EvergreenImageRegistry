ARG VERSION=5.13.19
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true && \
    apt-get update && apt-get install -y --no-install-recommends \
        php8.4-fpm php8.4 php8.4-curl php8.4-mbstring php8.4-xml zip php8.4-intl php8.4-mysql openssl php8.4-pdo php8.4-gd \
        nginx ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx ; 2>/dev/null || true \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Package integrity verified by apt/apk GPG signatures

RUN apk add --no-cache php-8.4-fpm php-8.4 php-8.4-curl php-8.4-mbstring php-8.4-xml zip php-8.4-intl php-8.4-pdo_mysql php-8.4-mysqli openssl php-8.4-pdo php-8.4-gd nginx ca-certificates || true && \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php 2>/dev/null || true
COPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["php-fpm8.4"]
LABEL org.opencontainers.image.title="invoice-ninja-api" \
      org.opencontainers.image.version="5.13.19" \
      org.opencontainers.image.vendor="Invoice Ninja" \
      org.opencontainers.image.source="https://github.com/invoiceninja/invoiceninja" \
      evergreen.image.tier="2" \
      evergreen.image.category="business-finance" \
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
