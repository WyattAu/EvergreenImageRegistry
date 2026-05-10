ARG VERSION=2.3.18

FROM cachethq/docker:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN addgroup -S -g 65532 cachet 2>/dev/null || true && \
    adduser -u 65532 -G cachet -D -s /bin/false cachet 2>/dev/null || true && \
    apk add --no-cache php-fpm php-pdo_mysql php-mysqli php-pgsql php-pdo_sqlite php-gd php-curl php-mbstring php-xml php-zip php-bcmath php-valkey nginx ca-certificates || true && \
    mkdir -p /var/www 2>/dev/null || true
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

LABEL org.opencontainers.image.title="cachet" org.opencontainers.image.version="2.3.18" org.opencontainers.image.vendor="CachetHQ" org.opencontainers.image.description="Cachet - open source status page system" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="5s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="30000ms" evergreen.hft.cpu-pins="2-3" evergreen.hft.cpu-pins-mode="shared" evergreen.hft.deploy-strategy="standard-rolling" evergreen.hft.pre-stop-hook="true" evergreen.hft.pre-stop-delay="10s" evergreen.hft.connection-drain="true" evergreen.hft.sched-policy="SCHED_OTHER" evergreen.hft.runtime="php" \
      org.opencontainers.image.source="https://github.com/CachetHQ/Cachet"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8000/ || exit 1
ENTRYPOINT ["/usr/sbin/php-fpm8.4", "-F"]
