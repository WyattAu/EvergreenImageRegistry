# =============================================================================

# EVERGREEN HARDENED PHP-FPM

# Generated from template - Version: 8.3

# Constraint: debian-slim - PHP-FPM runtime

# Priority: scratch > distroless > wolfi > debian-slim (fallback)

# =============================================================================



ARG VERSION=8.3

ARG BUILD_DATE





FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache curl \ || true && \
    php-8.4 php-8.4-fpm php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip

RUN adduser -u 65532 -D www-data 2>/dev/null || true && \

    mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true

USER 65532:65532

WORKDIR /app

EXPOSE 9000



HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9000/ || exit 1

ENTRYPOINT ["php-fpm"]

CMD ["-F"]

LABEL org.opencontainers.image.title="php-fpm" \

      org.opencontainers.image.description="php-fpm container image" \

      org.opencontainers.image.version="8.3" \

      org.opencontainers.image.vendor="PHP-FPM" \

      evergreen.image.tier="3" \

      evergreen.constraint.nonroot="true" \

      evergreen.base.image="wolfi" \

            org.opencontainers.image.source="https://github.com/php/php-src"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
