ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true

RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.4-fpm php8.4 php8.4-curl php8.4-gd php8.4-mbstring php8.4-xml zip php8.4-intl php8.4-mysql openssl php8.4-pdo json-c \
        nginx ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true

RUN mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx ; 2>/dev/null || true \
    mkdir -p /etc/nginx 2>/dev/null || true ; touch /etc/nginx/nginx.conf 2>/dev/null || true
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php 2>/dev/null || true

RUN apk add --no-cache php-8.4-fpm php-8.4 php-8.4-curl php-8.4-gd php-8.4-mbstring php-8.4-xml zip php-8.4-intl php-8.4-pdo_mysql php-8.4-mysqli openssl php-8.4-pdo json-c nginx ca-certificates 
RUN chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php 2>/dev/null || true
COPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf
    RUN chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/phpCOPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80 443
ENTRYPOINT ["php-fpm8.4"]
LABEL org.opencontainers.image.title="egroupware" \
      org.opencontainers.image.version="23.1.20240608" \
      org.opencontainers.image.vendor="EGroupware" \
      org.opencontainers.image.source="https://github.com/EGroupware/egroupware" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
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