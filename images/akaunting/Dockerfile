ARG VERSION=4.0.6
ARG TARGETARCH
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
# wolfi uses php-* not php84-*
RUN apk add --no-cache php-fpm php php-curl php-mbstring php-xml zip php-intl php-pdo_mysql php-mysqli openssl php-pdo nginx ca-certificates curl || true && \
    mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx && \
    chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["php-fpm"]
LABEL org.opencontainers.image.title="akaunting" \
      org.opencontainers.image.description="akaunting container image" \
      org.opencontainers.image.version="4.0.6" \
      org.opencontainers.image.vendor="Akaunting" \
      org.opencontainers.image.source="https://github.com/akaunting/akaunting" \
      evergreen.image.tier="2" \
      evergreen.image.category="business-finance" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
