# =============================================================================







# EVERGREEN HARDENED PHP-APACHE







# Generated from template - Version: 8.3







# Constraint: debian-slim - PHP + Apache2 runtime







# Priority: scratch > distroless > wolfi > debian-slim (fallback)







# =============================================================================















ARG VERSION=8.3
ARG TARGETARCH







ARG BUILD_DATE























FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9







RUN apk add --no-cache wget && \
    apache2 php-8.4 php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-pdo_mysql php-8.4-mysqli php-8.4-zip







RUN adduser -u 65532 -D www-data 2>/dev/null || true && \
    mkdir -p /app /var/log/apache2 /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/apache2 /var/log/php /var/cache/php 2>/dev/null || true







USER 65532:65532







WORKDIR /app







EXPOSE 80















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:80/ || exit 1







ENTRYPOINT ["apache2ctl"]







CMD ["-DFOREGROUND"]







LABEL org.opencontainers.image.title="php-apache" \
      org.opencontainers.image.description="php-apache container image" \
      org.opencontainers.image.version="8.3" \
      org.opencontainers.image.vendor="PHP/Apache" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/docker-library/official-images"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
