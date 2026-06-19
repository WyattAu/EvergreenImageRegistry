ARG VERSION=18.4
ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM postgres:${VERSION}
COPY --from=shim /shim /usr/local/bin/shim

# Override healthcheck to use shim TCP probe
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5432"]

# Keep upstream's docker-entrypoint.sh for initdb, user creation, etc.
# Shim wraps it for health monitoring + graceful shutdown
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "docker-entrypoint.sh"]
CMD ["postgres"]

ENV SHIM_METRICS_ENABLED="true"

EXPOSE 5432 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
LABEL org.opencontainers.image.title="postgresql-18" \
      org.opencontainers.image.version="18.4" \
      org.opencontainers.image.description="PostgreSQL 18 Database Server" \
      org.opencontainers.image.vendor="PostgreSQL Global Development Group" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://www.postgresql.org/" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGINT
