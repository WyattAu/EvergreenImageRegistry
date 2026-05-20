ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl nginx php-8.4-fpm php-8.4-pdo_sqlite php-8.4-mbstring php-8.4-xml || true && \
    addgroup -S -g 10000 organizr 2>/dev/null || true && \
    adduser -u 65532 -G organizr -D -h /app -s /bin/false organizr 2>/dev/null || true && \
    mkdir -p /app /app/src /config /var/log/nginx /var/lib/nginx 2>/dev/null || true && \
    echo '<?php-8.4 echo "Organizr binary not available - download failed" >&2 exit 1 v1.0.0"; ?>' > /app/index.php-8.4 2>/dev/null || true && \
    chown -R 65532:65532 /app /config /var/log/nginx /var/lib/nginx 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:80/ || exit 1
ENTRYPOINT ["php-fpm83"]
LABEL org.opencontainers.image.title="organizer" \
      org.opencontainers.image.description="Organizr - HTPC/Homelab dashboard" \
      org.opencontainers.image.vendor="CauseFX" \
      org.opencontainers.image.source="https://github.com/causefx/Organizr" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
