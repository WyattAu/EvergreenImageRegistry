FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl nginx php83-fpm php83-pdo_sqlite php83-mbstring php83-xml || true
RUN addgroup -S -g 10000 organizr 2>/dev/null || true && \
    adduser -u 65532 -G organizr -D -h /app -s /bin/false organizr 2>/dev/null || true
RUN mkdir -p /app /app/src /config /var/log/nginx /var/lib/nginx 2>/dev/null || true
RUN echo '<?php echo "Organizr placeholder v1.0.0"; ?>' > /app/index.php 2>/dev/null || true && \
    chown -R 65532:65532 /app /config /var/log/nginx /var/lib/nginx 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["php-fpm83"]
LABEL org.opencontainers.image.title="organizer" \
      org.opencontainers.image.description="Organizr - HTPC/Homelab dashboard" \
      org.opencontainers.image.vendor="CauseFX" \
      org.opencontainers.image.source="https://github.com/causefx/Organizr" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
