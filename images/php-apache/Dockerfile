# =============================================================================
# SOVEREIGN HARDENED PHP-APACHE
# Generated from template - Version: 8.3
# Constraint: debian-slim - PHP + Apache2 runtime
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.3
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates gnupg curl apache2 libapache2-mod-php8.3 && \
    curl -sSL https://packages.sury.org/php/apt.gnupg | gnupg --dearmor -o /usr/share/keyrings/sury-php.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gnupg] https://packages.sury.org/php/ $(. /etc/os-release && echo $VERSION_CODENAME) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    php8.3 php8.3-cli php8.3-common php8.3-curl php8.3-php84-mbstring php8.3-php84-xml php8.3-php84-mysql php8.3-zip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' www-data 2>/dev/null || true
RUN mkdir -p /app /var/log/apache2 /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/apache2 /var/log/php /var/cache/php 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["apache2ctl"]
CMD ["-DFOREGROUND"]
LABEL org.opencontainers.image.title="php-apache" \
      org.opencontainers.image.version="8.3" \
      org.opencontainers.image.vendor="PHP/Apache" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM