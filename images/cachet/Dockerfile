ARG VERSION=2.5.1

FROM cachethq/docker:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

RUN addgroup -S -g 65532 cachet 2>/dev/null || true
RUN adduser -u 65532 -G cachet -D -s /bin/false cachet 2>/dev/null || true
RUN apk add --no-cache php-8.4-fpm php-8.4-pdo_mysql php-8.4-mysqli php-8.4-pgsql php-8.4-pdo_sqlite php-8.4-gd php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip php-8.4-bcmath php-8.4-redis nginx ca-certificates || true
RUN mkdir -p /var/www 2>/dev/null || true
COPY --from=upstream /var/www/html /var/www/cachet
RUN mkdir -p /run/php /app/logs /app/data ; \
    chown -R cachet:cachet /var/www/cachet /app /run/php && \
    find /var/www/cachet -type d -exec chmod 755 {} \; && \
    find /var/www/cachet -type f -exec chmod 644 {} \; && \
    chmod +x /var/www/cachet/artisan 2>/dev/null || true
COPY <<'EOF' /etc/nginx/sites-available/cachet
server {
    listen 8000;
    root /var/www/cachet/public;
    index index.php;
    server_name _;
    location / {
        try_files $uri /index.php$is_args$args;
    }
    location ~ \.php$ {
        fastcgi_pass unix:/run/php/php84-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
EOF
RUN ln -sf /etc/nginx/sites-available/cachet /etc/nginx/sites-enabled/cachet && \
    rm -f /etc/nginx/sites-enabled/default

ENV APP_ENV=production APP_DEBUG=false DB_DRIVER=sqlite CACHE_DRIVER=file SESSION_DRIVER=file

WORKDIR /app

EXPOSE 8000
EXPOSE 9101

LABEL org.opencontainers.image.title="cachet" org.opencontainers.image.version="2.5.1" org.opencontainers.image.vendor="CachetHQ" org.opencontainers.image.description="Cachet - open source status page system" sovereign.image.tier="1" sovereign.constraint.nonroot="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="5s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="30000ms" sovereign.hft.cpu-pins="2-3" sovereign.hft.cpu-pins-mode="shared" sovereign.hft.deploy-strategy="standard-rolling" sovereign.hft.pre-stop-hook="true" sovereign.hft.pre-stop-delay="10s" sovereign.hft.connection-drain="true" sovereign.hft.sched-policy="SCHED_OTHER" sovereign.hft.runtime="php"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/usr/sbin/php-fpm8.4", "-F"]
