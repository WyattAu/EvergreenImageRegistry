ARG VERSION=1.29.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM freshrss/freshrss:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache ca-certificates nginx php-8.4 php-8.4-fpm php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip php-8.4-pgsql php-8.4-mysqlnd php-8.4-gd php-8.4-intl && \
    mkdir -p /var/log/nginx /var/cache/nginx /run /var/log/php /var/cache/php && \
    chown -R 65532:65532 /var/log/nginx /var/cache/nginx /run /var/log/php /var/cache/php

# Copy FreshRSS application from upstream
COPY --from=upstream /var/www/FreshRSS /var/www/FreshRSS
RUN chown -R 65532:65532 /var/www/FreshRSS

# Nginx config: serve FreshRSS via PHP-FPM on port 8080
RUN printf 'events {}\n\
http {\n\
  server {\n\
    listen 8080;\n\
    root /var/www/FreshRSS/p;\n\
    index index.php index.html;\n\
    location / { try_files $uri $uri/ /index.php?$query_string; }\n\
    location ~ \\.php$ {\n\
      fastcgi_pass 127.0.0.1:9000;\n\
      fastcgi_index index.php;\n\
      fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;\n\
      include fastcgi_params;\n\
    }\n\
  }\n\
}\n' > /etc/nginx/nginx.conf

# PHP-FPM config for non-root
RUN sed -i 's/^user = .*/user = 65532/' /etc/php/8.4/php-fpm.d/www.conf 2>/dev/null || \
    sed -i 's/^user = .*/user = 65532/' /etc/php84/php-fpm.d/www.conf 2>/dev/null || true && \
    sed -i 's/^group = .*/group = 65532/' /etc/php/8.4/php-fpm.d/www.conf 2>/dev/null || \
    sed -i 's/^group = .*/group = 65532/' /etc/php84/php-fpm.d/www.conf 2>/dev/null || true && \
    sed -i 's/^listen = .*/listen = 127.0.0.1:9000/' /etc/php/8.4/php-fpm.d/www.conf 2>/dev/null || \
    sed -i 's/^listen = .*/listen = 127.0.0.1:9000/' /etc/php84/php-fpm.d/www.conf 2>/dev/null || true

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/www/FreshRSS
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

# Start both PHP-FPM and nginx via a shell wrapper
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "sh -c 'php-fpm84 -F & nginx -g \"daemon off;\"'"]

LABEL org.opencontainers.image.title="freshrss" \
      org.opencontainers.image.description="FreshRSS - self-hosted RSS feed reader" \
      org.opencontainers.image.version="1.29.0" \
      org.opencontainers.image.vendor="FreshRSS" \
      org.opencontainers.image.source="https://github.com/FreshRSS/FreshRSS" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true"
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
