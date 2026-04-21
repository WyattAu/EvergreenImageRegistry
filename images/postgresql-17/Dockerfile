# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL 17
# Generated from template - Version: 17.2
# Constraint: debian-slim - PostgreSQL requires glibc + shared libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 lsb-release curl ca-certificates && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > \
    /etc/apt/sources.list.d/pgdg.list && \
    curl -fsSL "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | \
    gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg && \
    apt-get update && apt-get install -y --no-install-recommends \
    postgresql-${VERSION%.*} postgresql-contrib-${VERSION%.*} && \
    mkdir -p /var/lib/postgresql/data /var/run/postgresql /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 lsb-release curl ca-certificates libreadline8 libzstd1 liblz4-1 libicu72 && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > \
    /etc/apt/sources.list.d/pgdg.list && \
    curl -fsSL "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | \
    gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg && \
    apt-get update && apt-get install -y --no-install-recommends \
    postgresql-${VERSION%.*} postgresql-contrib-${VERSION%.*} && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /var/lib/postgresql /var/lib/postgresql
COPY --from=builder /var/run/postgresql /var/run/postgresql
RUN usermod -u 65534 postgres && \
    mkdir -p /app /var/log/postgresql-17 /var/cache/postgresql-17 && \
    chown -R 65534:65534 /var/lib/postgresql /var/run/postgresql /app /var/log/postgresql-17 /var/cache/postgresql-17
USER 65534:65534
WORKDIR /app
ENV PGDATA="/var/lib/postgresql/data" \
    PGPORT="5432"
EXPOSE 5432
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["pg_isready", "-h", "localhost"]
ENTRYPOINT ["postgres"]
LABEL org.opencontainers.image.title="postgresql-17" \
      org.opencontainers.image.version="17.2" \
      org.opencontainers.image.description="PostgreSQL 17 Database Server" \
      org.opencontainers.image.vendor="PostgreSQL Global Development Group" \
      org.opencontainers.image.source="https://www.postgresql.org/" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
