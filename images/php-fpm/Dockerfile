# =============================================================================
# SOVEREIGN HARDENED PHP-FPM
# Generated from template - Version: 8.3
# Constraint: debian-slim - PHP-FPM runtime
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.3
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates gnupg2 curl && \
    curl -sSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ $(. /etc/os-release && echo $VERSION_CODENAME) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    php8.3-fpm php8.3-cli php8.3-common php8.3-curl php8.3-mbstring php8.3-xml php8.3-zip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 9000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["php-fpm8.3", "--version"]
ENTRYPOINT ["php-fpm8.3"]
CMD ["-F"]
LABEL org.opencontainers.image.title="php-fpm" \
      org.opencontainers.image.version="8.3" \
      org.opencontainers.image.vendor="PHP-FPM" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
