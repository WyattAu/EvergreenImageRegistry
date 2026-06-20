ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG NGINX_VERSION=1.27.1
ARG MODSEC_VERSION=3.0.12

RUN apk add --no-cache nginx ca-certificates libxml2 curl && \
    addgroup -S -g 10000 nginx 2>/dev/null || true && \
    adduser -u 65532 -G nginx -D -h /app -s /bin/false nginx 2>/dev/null || true && \
    mkdir -p /app /var/log/nginx /var/cache/nginx /etc/nginx/modsec /run 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/nginx /var/cache/nginx 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 80 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "nginx"]
CMD ["--", "-g", "daemon off;"]
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
