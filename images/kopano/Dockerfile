# =============================================================================
# SOVEREIGN HARDENED KOPANO
# Generated from template - Version: 12.1.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=12.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates gnupg2 curl && \
    curl -sSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ $(. /etc/os-release && echo $VERSION_CODENAME) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    php8.3 php8.3-fpm php8.3-curl php8.3-mbstring php8.3-xml php8.3-zip php8.3-gd php8.3-mysql php8.3-soap && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:80/
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="kopano" \
      org.opencontainers.image.version="12.1.0" \
      org.opencontainers.image.vendor="Kopano-dev/kopano-core" \
      org.opencontainers.image.source="https://github.com/Kopano-dev/kopano-core/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
