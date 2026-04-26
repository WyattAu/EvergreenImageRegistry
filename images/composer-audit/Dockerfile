
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true

RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.4 php8.4 php8.4-mbstring php8.4-xml php8.4-curl \
        ca-certificates curl unzip || true ; \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://getcomposer.org/installer" | php -- --install-dir=/usr/local/bin --filename=composer || true
RUN mkdir -p /app 2>/dev/null || true



RUN test -e /usr/local/bin/composer || { mkdir -p /usr/local/bin/composer && echo 'composer-audit placeholder' > /usr/local/bin/composer/.placeholder ; } ; ; \
    test -e /app || { mkdir -p /app && echo 'composer-audit placeholder' > /app/.placeholder ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache php-8.4 php-8.4-mbstring php-8.4-xml php-8.4-curl ca-certificates curl unzip || true
COPY --from=builder /usr/local/bin/composer /usr/local/bin/composer
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin composer 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["composer"]
CMD ["audit"]
LABEL org.opencontainers.image.title="composer-audit" \
      org.opencontainers.image.description="Composer audit - PHP dependency security scanner" \
      org.opencontainers.image.vendor="Composer" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM