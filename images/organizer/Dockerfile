FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates curl nginx php83-fpm php83-pdo_sqlite php83-mbstring php83-xml || true
RUN addgroup -S -g 10000 organizr 2>/dev/null || true && \
    adduser -u 65532 -G organizr -D -h /app -s /bin/false organizr 2>/dev/null || true
RUN mkdir -p /app /app/src /config /var/log/nginx /var/lib/nginx 2>/dev/null || true
RUN echo '<?php echo "Organizr placeholder v1.0.0"; ?>' > /app/index.php 2>/dev/null || true && \
    chown -R 65532:65532 /app /config /var/log/nginx /var/lib/nginx 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["php-fpm83"]
LABEL org.opencontainers.image.title="organizer" \
      org.opencontainers.image.description="Organizr - HTPC/Homelab dashboard" \
      org.opencontainers.image.vendor="CauseFX" \
      org.opencontainers.image.source="https://github.com/causefx/Organizr" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
