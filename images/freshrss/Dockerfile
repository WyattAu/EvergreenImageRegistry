# =============================================================================
# SOVEREIGN HARDENED FRESHRSS
# Generated from template - Version: 1.24.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.24.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates gnupg curl && \
    curl -sSL https://packages.sury.org/php/apt.gnupg | gnupg --dearmor -o /usr/share/keyrings/sury-php.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gnupg] https://packages.sury.org/php/ $(. /etc/os-release && echo $VERSION_CODENAME) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    php8.3 php8.3-fpm php8.3-curl php8.3-php84-mbstring php8.3-php84-xml php8.3-zip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true
USER www-data
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["php"]
LABEL org.opencontainers.image.title="freshrss" \
      org.opencontainers.image.version="1.24.1" \
      org.opencontainers.image.vendor="FreshRSS" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM