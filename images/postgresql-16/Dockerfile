ARG VERSION=16
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

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
LABEL org.opencontainers.image.title="postgresql-16" \
      org.opencontainers.image.description="PostgreSQL 16 - hardened with Evergreen health-shim" \
      evergreen.image.tier="critical" \
      evergreen.constraint.hardened="true"
LABEL evergreen.base.image="upstream"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
STOPSIGNAL SIGINT
