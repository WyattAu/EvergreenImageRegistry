# =============================================================================
# EVERGREEN HARDENED APACHE HTTPD
# Apache HTTP Server on debian-slim
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=2.4.66
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=2.4.66
RUN apk add --no-cache apache2 ca-certificates tzdata && \
    a2dismod autoindex 2>/dev/null || true && \
    addgroup -S -g 65532 www-data 2>/dev/null || true && \
    usermod -u 65532 www-data 2>/dev/null || true && \
    chown -R 65532:65532 /var/www/html /var/log/apache2 /var/run/apache2 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/www/html
EXPOSE 80 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "apache2ctl", "--", "-D", "FOREGROUND"]
LABEL org.opencontainers.image.title="apache" \
      org.opencontainers.image.description="apache container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Apache Software Foundation" \
      org.opencontainers.image.source="https://httpd.apache.org" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="webserver" \
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
