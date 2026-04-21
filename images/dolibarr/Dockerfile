# =============================================================================
# SOVEREIGN HARDENED DOLIBARR
# Generated from template - Version: 23.0.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=23.0.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates gnupg2 curl && \
    curl -sSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ $(. /etc/os-release && echo $VERSION_CODENAME) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    php8.3 php8.3-fpm php8.3-mysql php8.3-curl php8.3-mbstring php8.3-xml php8.3-zip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Dolibarr/dolibarr/archive/refs/tags/${VERSION}.tar.gz" -o /tmp/dolibarr.tar.gz && \
    tar -xzf /tmp/dolibarr.tar.gz -C /opt && mv /opt/dolibarr-${VERSION} /opt/dolibarr && rm /tmp/dolibarr.tar.gz
RUN useradd -m -u 65534 -g '' www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/dolibarr /var/cache/dolibarr && chown -R www-data:www-data /app /var/log/dolibarr /var/cache/dolibarr /opt/dolibarr 2>/dev/null || true
USER www-data
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:80
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="dolibarr" \
      org.opencontainers.image.version="23.0.2" \
      org.opencontainers.image.vendor="Dolibarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
