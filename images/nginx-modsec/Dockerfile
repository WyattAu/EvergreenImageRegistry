FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG NGINX_VERSION=1.27.1
ARG MODSEC_VERSION=3.0.12

RUN apk add --no-cache nginx ca-certificates libxml2 curl || true && \
    addgroup -S -g 10000 nginx 2>/dev/null || true && \
    adduser -u 65532 -G nginx -D -h /app -s /bin/false nginx 2>/dev/null || true && \
    mkdir -p /app /var/log/nginx /var/cache/nginx /etc/nginx/modsec /run 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/nginx /var/cache/nginx 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
LABEL org.opencontainers.image.title="nginx-modsec" \
      org.opencontainers.image.version="1.27.1" \
      org.opencontainers.image.vendor="NGINX Inc / SpiderLabs" \
      org.opencontainers.image.source="https://github.com/SpiderLabs/ModSecurity" \
      org.opencontainers.image.description="NGINX with ModSecurity WAF module" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
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
