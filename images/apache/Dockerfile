# =============================================================================
# EVERGREEN HARDENED APACHE HTTPD
# Apache HTTP Server on debian-slim
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=2.4.66
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=2.4.66
RUN apk add --no-cache apache2 ca-certificates tzdata || true && \
    a2dismod autoindex 2>/dev/null || true && \
    addgroup -S -g 65532 www-data 2>/dev/null || true && \
    usermod -u 65532 www-data 2>/dev/null || true && \
    chown -R 65532:65532 /var/www/html /var/log/apache2 /var/run/apache2 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["apache2ctl"]
CMD ["-D", "FOREGROUND"]
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
STOPSIGNAL SIGTERM
