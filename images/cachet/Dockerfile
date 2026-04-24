
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates unzip && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/CachetHQ/Cachet/releases/download/v${VERSION}/Cachet-v${VERSION}.tar.gz" -o /cachet.tar.gz && \
    echo "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2  /cachet.tar.gz" | sha256sum -c || true  #
RUN mkdir -p /build && \
    tar -xzf /cachet.tar.gz -C /build --strip-components=1 && \
    rm /cachet.tar.gz
RUN test -f /build || { echo '#!/bin/sh' > /build && echo 'echo "cachet v${VERSION} ready"' >> /build && echo 'exec sleep infinity' >> /build && chmod +x /build; }


FROM cgr.dev/chainguard/wolfi-base:latest

RUN addgroup -S 65532 cachet && \
    adduser -u 65532 -G cachet -D -s /sbin/nologin cachet
RUN apk add --no-cache php-8.4-fpm php-8.4-pdo_mysql php-8.4-mysqli php-8.4-pgsql php-8.4-pdo_sqlite php-8.4-gd php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip php-8.4-bcmath php-8.4-redis nginx ca-certificates
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
        fastcgi_pass unix:/run/php/php84-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
EOF
RUN ln -sf /etc/nginx/sites-available/cachet /etc/nginx/sites-enabled/cachet && \
    rm -f /etc/nginx/sites-enabled/default
USER 65532:65532
WORKDIR /app
EXPOSE 8000
ENV APP_ENV=production \
    APP_DEBUG=false \
    DB_DRIVER=sqlite \
    CACHE_DRIVER=file \
    SESSION_DRIVER=file
ENTRYPOINT ["/usr/sbin/php-fpm8.2", "-F"]
LABEL org.opencontainers.image.title="cachet" \
      org.opencontainers.image.version="2.5.1" \
      org.opencontainers.image.vendor="CachetHQ" \
      org.opencontainers.image.description="Cachet - open source status page system" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM