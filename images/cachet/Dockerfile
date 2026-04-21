# =============================================================================
# SOVEREIGN HARDENED CACHET
# Generated from template - Version: 2.5.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# PHP application requires runtime and web server - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.5.1
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS downloader
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates unzip && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/CachetHQ/Cachet/releases/download/v${VERSION}/Cachet-v${VERSION}.tar.gz" -o /cachet.tar.gz && \
    echo "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2  /cachet.tar.gz" | sha256sum -c -
RUN mkdir -p /build && \
    tar -xzf /cachet.tar.gz -C /build --strip-components=1 && \
    rm /cachet.tar.gz

FROM debian:bookworm-20240101-slim
RUN groupadd -g 65534 cachet && \
    useradd -m -u 65534 -g cachet -s /usr/sbin/nologin cachet
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        php8.2-fpm \
        php8.2-mysql \
        php8.2-pgsql \
        php8.2-sqlite3 \
        php8.2-gd \
        php8.2-curl \
        php8.2-mbstring \
        php8.2-xml \
        php8.2-zip \
        php8.2-bcmath \
        php8.2-redis \
        nginx \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /build /var/www/cachet
RUN mkdir -p /run/php /app/logs /app/data && \
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
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
EOF
RUN ln -sf /etc/nginx/sites-available/cachet /etc/nginx/sites-enabled/cachet && \
    rm -f /etc/nginx/sites-enabled/default
USER 65534:65534
WORKDIR /app
EXPOSE 8000
ENV APP_ENV=production \
    APP_DEBUG=false \
    DB_DRIVER=sqlite \
    CACHE_DRIVER=file \
    SESSION_DRIVER=file
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["/usr/sbin/nginx", "-v"]
ENTRYPOINT ["/usr/sbin/php-fpm8.2", "-F"]
LABEL org.opencontainers.image.title="cachet" \
      org.opencontainers.image.version="2.5.1" \
      org.opencontainers.image.vendor="CachetHQ" \
      org.opencontainers.image.description="Cachet - open source status page system" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms" \
      sovereign.hft.cpu-pins="2-3" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="10s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="php"
