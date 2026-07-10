ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/mariadb:latest
USER 0
COPY --from=shim /shim /usr/local/bin/shim
RUN chown -R 65532:65532 /var/lib/mysql /var/run/mysqld 2>/dev/null || true
USER 65532

ENV SHIM_METRICS_ENABLED="true"

EXPOSE 3306 9101
VOLUME /var/lib/mysql

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3306"]

LABEL org.opencontainers.image.title="mariadb" \
      org.opencontainers.image.description="MariaDB - Chainguard wolfi-base, non-root UID 65532, health shim" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true"
LABEL evergreen.base.image="wolfi-base"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
LABEL evergreen.entrypoint.pattern="chainguard-repack"
STOPSIGNAL SIGTERM
