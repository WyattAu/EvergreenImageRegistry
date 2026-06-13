# =============================================================================
# EVERGREEN HARDENED IMMICH-POSTGRES
# PostgreSQL 16 with pgvector extension for Immich
# Constraint: wolfi-base hardened multi-stage
# =============================================================================
ARG VERSION=16.6
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.1.0

FROM cgr.dev/chainguard/wolfi-base AS builder
ARG VERSION
RUN apk add --no-cache gcc make glibc-dev linux-headers ca-certificates wget git \
    postgresql-16-dev
# Build pgvector from source
RUN wget -q https://github.com/pgvector/pgvector/archive/refs/tags/v0.8.0.tar.gz -O pgvector.tar.gz && \
    tar xzf pgvector.tar.gz && cd pgvector-0.8.0 && \
    make && make install

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base
ARG APP_UID
ARG APP_GID
ARG VERSION
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /usr/share/postgresql-16/extension/vector* /usr/share/postgresql-16/extension/
COPY --from=builder /usr/lib/postgresql-16/lib/vector.so /usr/lib/postgresql-16/lib/
RUN apk add --no-cache postgresql-16 && \
    mkdir -p /var/lib/postgresql/data /var/run/postgresql && \
    chown -R ${APP_UID}:${APP_GID} /var/lib/postgresql /var/run/postgresql
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER ${APP_UID}:${APP_GID}
ENV PGDATA=/var/lib/postgresql/data \
    PATH="/usr/lib/postgresql-16/bin:$PATH"
EXPOSE 5432 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5432"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "postgres"]
CMD ["-D", "/var/lib/postgresql/data"]
LABEL org.opencontainers.image.title="immich-postgres" \
      org.opencontainers.image.description="PostgreSQL 16 with pgvector extension for Immich" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Immich" \
      org.opencontainers.image.source="https://github.com/pgvector/pgvector" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
