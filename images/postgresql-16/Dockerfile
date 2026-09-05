ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/postgres:16.4
USER 0
COPY --from=shim /shim /usr/local/bin/shim
# Ensure /var/lib/postgresql is owned by postgres (UID 70 in wolfi)
RUN chown -R 70:70 /var/lib/postgresql /var/run/postgresql 2>/dev/null || true
USER 70

ENV SHIM_METRICS_ENABLED="true" \
    PGDATA=/var/lib/postgresql/data

EXPOSE 54332 9101
VOLUME /var/lib/postgresql/data

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \

  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5432"]

LABEL org.opencontainers.image.title="postgresql-16" \
      org.opencontainers.image.description="PostgreSQL 16 - Chainguard wolfi-base, non-root, health shim" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true"
LABEL evergreen.base.image="wolfi-base"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
LABEL evergreen.entrypoint.pattern="chainguard-repack"
STOPSIGNAL SIGINT
LABEL evergreen.security.read-only-rootfs="false"
