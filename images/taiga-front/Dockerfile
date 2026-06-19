ARG VERSION=6.9.0
ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM taigaio/taiga-front:${VERSION} AS upstream

FROM upstream
COPY --from=shim /shim /usr/local/bin/shim

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "nginx -g 'daemon off;'"]

LABEL org.opencontainers.image.title="taiga-front" \
      org.opencontainers.image.description="Taiga Front - Angular SPA for project management" \
      org.opencontainers.image.version="6.9.0" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-front-dist" \
      evergreen.image.tier="2" \
      evergreen.image.category="project-management" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
