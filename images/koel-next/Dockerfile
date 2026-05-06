# =============================================================================







# EVERGREEN HARDENED KOEL-NEXT







# Generated from template - Version: 6.10.3







# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable







# Priority: scratch > distroless > wolfi > debian-slim (last resort)







# =============================================================================















ARG VERSION=6.10.3







ARG BUILD_DATE























FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31







ARG GITHUB_TOKEN







RUN apk add --no-cache curl
    php-8.4 php-8.4-fpm php-8.4-curl php-8.4-mbstring php-8.4-xml php-8.4-zip php-8.4-gd php-8.4-pdo_mysql php-8.4-mysqli php-8.4-pdo_sqlite php-8.4-bcmath







RUN adduser -u 65532 -D www-data 2>/dev/null || true && \
    mkdir -p /app /var/log/php /var/cache/php && chown -R www-data:www-data /app /var/log/php /var/cache/php 2>/dev/null || true







USER 65532:65532







WORKDIR /app







EXPOSE 80















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1







ENTRYPOINT ["php"]







LABEL org.opencontainers.image.title="koel-next" \
      org.opencontainers.image.description="koel-next container image" \
      org.opencontainers.image.version="6.10.3" \
      org.opencontainers.image.vendor="koel/koel" \
      org.opencontainers.image.source="https://github.com/koel/koel/releases" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
