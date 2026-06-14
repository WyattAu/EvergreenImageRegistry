ARG VERSION=3.1.21-v
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM akaunting/akaunting:latest AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# wolfi uses php-* not php84-*
RUN apk add --no-cache ca-certificates curl nginx \
        php-8.4 php-8.4-fpm php-8.4-curl php-8.4-mbstring php-8.4-xml \
        php-8.4-zip php-8.4-intl php-8.4-pdo php-8.4-pdo_mysql php-8.4-mysqli \
        php-8.4-gd php-8.4-fileinfo php-8.4-bcmath php-8.4-opcache openssl && \
    mkdir -p /var/log/nginx /var/cache/nginx /run /var/log/php /var/cache/php /var/lib/nginx/{logs,tmp} /var/www/html/storage/framework/{sessions,views,cache} /var/www/html/bootstrap/cache && \
    chown -R 65532:65532 /var/log/nginx /var/cache/nginx /run /var/log/php /var/cache/php /var/lib/nginx /var/www

# Copy Akaunting application from upstream
COPY --from=upstream /var/www/html /var/www/html
RUN chown -R 65532:65532 /var/www/html && \
    chmod -R u+rwX /var/www/html/storage /var/www/html/bootstrap/cache

# Nginx config: serve Akaunting (Laravel) via PHP-FPM on port 8080
RUN printf 'events {}\n\
http {\n\
  include /etc/nginx/fastcgi_params;\n\
  client_max_body_size 25M;\n\
  server {\n\
    listen 8080;\n\
    root /var/www/html/public;\n\
    index index.php index.html;\n\
    location / { try_files $uri $uri/ /index.php?$query_string; }\n\
    location ~ \\.php$ {\n\
      fastcgi_pass 127.0.0.1:9000;\n\
      fastcgi_index index.php;\n\
      fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;\n\
      include fastcgi_params;\n\
    }\n\
    location ~ /\\.ht { deny all; }\n\
  }\n\
}\n' > /etc/nginx/nginx.conf

# PHP-FPM config for non-root (wolfi path: /etc/php)
RUN sed -i 's/^user = .*/user = 65532/' /etc/php/php-fpm.d/www.conf && \
    sed -i 's/^group = .*/group = 65532/' /etc/php/php-fpm.d/www.conf && \
    sed -i 's/^listen = .*/listen = 127.0.0.1:9000/' /etc/php/php-fpm.d/www.conf && \
    sed -i 's/^;daemonize = .*/daemonize = no/' /etc/php/php-fpm.conf && \
    printf '[www]\nlisten = 127.0.0.1:9000\n' > /etc/php/php-fpm.d/zz-evergreen.conf

# Startup script: launch PHP-FPM and nginx
RUN printf '#!/bin/sh\nphp-fpm -F &\nnginx -g "daemon off;"\n' > /usr/local/bin/start-app.sh && \
    chmod +x /usr/local/bin/start-app.sh

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/www/html
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

# Start both PHP-FPM and nginx via startup script
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/start-app.sh"]

LABEL org.opencontainers.image.title="akaunting" \
      org.opencontainers.image.description="Akaunting - online accounting software" \
      org.opencontainers.image.version="3.1.21-v" \
      org.opencontainers.image.vendor="Akaunting" \
      org.opencontainers.image.source="https://github.com/akaunting/akaunting" \
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
