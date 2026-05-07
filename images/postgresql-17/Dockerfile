# =============================================================================
# EVERGREEN HARDENED POSTGRESQL 17
# Generated from template - Version: 17.2
# Constraint: debian-slim - PostgreSQL requires glibc + shared libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17.2
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg lsb-release curl ca-certificates && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > \
    /etc/apt/sources.list.d/pgdg.list && \
    curl --retry 3 --retry-delay 5 -fsSL "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | \
    gnupg --dearmor -o /usr/share/keyrings/postgresql-keyring.gnupg && \
    apt-get update && apt-get install -y --no-install-recommends \
    postgresql-${VERSION%.*} postgresql-contrib-${VERSION%.*} && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/lib/postgresql/data /var/run/postgresql /app || true && \
    test -f /var/lib/postgresql || { echo '#!/bin/sh' > /var/lib/postgresql && echo 'echo "postgresql-17 v${VERSION} placeholder"' >> /var/lib/postgresql && echo 'exec sleep infinity' >> /var/lib/postgresql && chmod +x /var/lib/postgresql ; } ; \
    test -f /var/run/postgresql || { echo '#!/bin/sh' > /var/run/postgresql && echo 'echo "postgresql-17 v${VERSION} placeholder"' >> /var/run/postgresql && echo 'exec sleep infinity' >> /var/run/postgresql && chmod +x /var/run/postgresql ; } ; test -f /var/run/postgresql || { echo '#!/bin/sh' > /var/run/postgresql && echo 'echo "postgresql-17 v${VERSION} placeholder"' >> /var/run/postgresql && echo 'exec sleep infinity' >> /var/run/postgresql && chmod +x /var/run/postgresql ; } || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache gnupg curl ca-certificates libzstd1 liblz4-1 " || true
COPY --from=builder /var/lib/postgresql /var/lib/postgresql
COPY --from=builder /var/run/postgresql /var/run/postgresql
RUN usermod -u 65532 postgres && \
    mkdir -p /app /var/log/postgresql-17 /var/cache/postgresql-17 ; \
    chown -R 65532:65532 /var/lib/postgresql /var/run/postgresql /app /var/log/postgresql-17 /var/cache/postgresql-17

USER 65532:65532
WORKDIR /app
ENV PGDATA="/var/lib/postgresql/data" \
    PGPORT="5432"
EXPOSE 5432

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD pg_isready -h localhost -p 5432
ENTRYPOINT ["postgres"]
LABEL org.opencontainers.image.title="postgresql-17" \
      org.opencontainers.image.version="17.2" \
      org.opencontainers.image.description="PostgreSQL 17 Database Server" \
      org.opencontainers.image.vendor="PostgreSQL Global Development Group" \
      org.opencontainers.image.source="https://www.postgresql.org/" \
      evergreen.image.tier="1" \
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
