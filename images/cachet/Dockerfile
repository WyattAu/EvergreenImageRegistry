ARG VERSION=2.3.18
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS upstream
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && \
    apt-get install -y --no-install-recommends \
        php-cli php-curl php-mbstring php-xml php-zip php-bcmath php-gd \
        php-mysql php-pgsql php-sqlite3 && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/CachetHQ/Cachet/archive/refs/tags/v${VERSION}.tar.gz" \
        -o /tmp/cachet.tar.gz ; \
    mkdir -p /var/www/cachet && \
    tar -xzf /tmp/cachet.tar.gz -C /tmp ; \
    cp -a /tmp/Cachet-${VERSION}/* /var/www/cachet/ 2>/dev/null ; \
    EXPECTED_SIGNATURE=$(curl -fsSL https://composer.github.io/installer.sig) ; \
    curl -fsSL https://getcomposer.org/installer -o /tmp/composer-setup.php 2>/dev/null ; \
    php /tmp/composer-setup.php --install-dir=/usr/local/bin --filename=composer 2>/dev/null || true ; \
    cd /var/www/cachet && composer install --no-dev --optimize-autoloader 2>/dev/null || true ; \
    mkdir -p /run/php && \
    rm -rf /tmp/cachet.tar.gz /tmp/Cachet-${VERSION} /tmp/composer-setup.php /var/lib/apt/lists/*
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN addgroup -S -g 65532 cachet 2>/dev/null || true && \
    adduser -u 65532 -G cachet -D -s /bin/false cachet 2>/dev/null || true && \
     apk add --no-cache php-8.4-fpm php-8.4-pdo_mysql php-8.4-mysqli php-8.4-pgsql php-8.4-pdo_sqlite php-8.4-gd php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip php-8.4-bcmath php-8.4-redis nginx ca-certificates curl && \
    mkdir -p /var/www 2>/dev/null || true
RUN mkdir -p /var/www/cachet || true
COPY --from=upstream /var/www/cachet /var/www/cachet
RUN mkdir -p /run/php /var/log/nginx /app/logs /app/data && \
    chown -R cachet:cachet /var/www/cachet /app /run/php 2>/dev/null || true && \
    find /var/www/cachet -type d -exec chmod 755 {} \; && \
    find /var/www/cachet -type f -exec chmod 644 {} \; && \
    chmod +x /var/www/cachet/artisan 2>/dev/null
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
        fastcgi_pass unix:/run/php/php-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
EOF
RUN ln -sf /etc/nginx/sites-available/cachet /etc/nginx/sites-enabled/cachet && \
    rm -f /etc/nginx/sites-enabled/default
ENV APP_ENV=production APP_DEBUG=false DB_DRIVER=sqlite CACHE_DRIVER=file SESSION_DRIVER=file
WORKDIR /app
EXPOSE 8000 9101
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
ENV SHIM_METRICS_ENABLED="true"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
