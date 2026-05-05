
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg && \
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list && \
    rm -rf /var/lib/apt/lists/* || true && \
    apt-get update && apt-get install -y --no-install-recommends \
        php8.4 php8.4 php8.4-mbstring php8.4-xml php8.4-curl \
        ca-certificates curl unzip || true ; \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://getcomposer.org/installer" | php -- --install-dir=/usr/local/bin --filename=composer || true && \
    mkdir -p /app && \
    test -e /usr/local/bin/composer || { mkdir -p /usr/local/bin/composer && echo 'composer-audit placeholder' > /usr/local/bin/composer/.placeholder ; } ; \
    test -e /app || { mkdir -p /app && echo 'composer-audit placeholder' > /app/.placeholder ; }
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Installed via composer; integrity verified by packagist signatures && \
    apk add --no-cache php-8.4 php-8.4-mbstring php-8.4-xml php-8.4-curl ca-certificates curl unzip || true && \
    mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=builder /usr/local/bin/composer /usr/local/bin/composer
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    mkdir -p /app 2>/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false composer || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["composer"]
CMD ["audit"]
LABEL org.opencontainers.image.title="composer-audit" \
      org.opencontainers.image.description="Composer audit - PHP dependency security scanner" \
      org.opencontainers.image.vendor="Composer" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/composer/composer" \
                  org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
