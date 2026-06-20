# =============================================================================







# EVERGREEN HARDENED CADDY-ALPINE







# Caddy web server with automatic HTTPS







# Constraint: wolfi - hardened minimal base







# =============================================================================















ARG VERSION=2.8.4







ARG TARGETARCH







ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532























ARG SHIM_VERSION=v1.2.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS downloader







ARG VERSION=2.8.4







RUN apk add --no-cache curl ca-certificates && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/caddyserver/caddy/releases/download/v${VERSION}/caddy_${VERSION}_linux_${TARGETARCH}.tar.gz" -o /caddy.tar.gz ; \
    echo "a7e8306c54138cf88e371c5ec0caf7baf142ecc1d60a30897dfb67d65d3748c8  /caddy.tar.gz" | sha256sum -c; \
    if [ -f /caddy.tar.gz ]; then tar -xzf /caddy.tar.gz -C / && rm -f /caddy.tar.gz ; fi ; \
    chmod +x /caddy 2>/dev/null ; \' && { echo "Binary not available - download failed" >&2; exit 1; }























FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim








ARG VERSION=2.8.4







RUN apk add --no-cache ca-certificates libcap && \
    mkdir -p /app /var/log/caddy /var/cache/caddy /var/lib/caddy







COPY --from=downloader /caddy /usr/local/bin/caddy







RUN chown -R 65532:65532 /app /var/log/caddy /var/cache/caddy /var/lib/caddy && \
    setcap cap_net_bind_service=+ep /usr/local/bin/caddy 2>/dev/null || true







USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"







WORKDIR /app







EXPOSE 80 443 443/udp 2019






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/caddy"]







CMD ["--", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]







LABEL org.opencontainers.image.title="caddy-alpine" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Caddy Server" \
      org.opencontainers.image.source="https://github.com/caddyserver/caddy" \
      org.opencontainers.image.description="Caddy web server with automatic HTTPS" \
      evergreen.image.tier="1" \
      evergreen.image.category="webserver" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.base.image="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"















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
