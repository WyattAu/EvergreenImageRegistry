# =============================================================================
# SOVEREIGN HARDENED MARIADB-GALERA
# Constraint: debian-slim - native database + Galera cluster package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=11.4.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://mariadb.org/mariadb_release_signing_key.asc" | gnupg --dearmor -o /usr/share/keyrings/mariadb-keyring.gnupg \
    && echo "deb [signed-by=/usr/share/keyrings/mariadb-keyring.gnupg] http://mirror.mariadb.org/repo/11.4/debian bookworm main" > /etc/apt/sources.list.d/mariadb.list

FROM cgr.dev/chainguard/wolfi-base:latest

COPY --from=builder /usr/share/keyrings/mariadb-keyring.gnupg /usr/share/keyrings/mariadb-keyring.gnupg
COPY --from=builder /etc/apt/sources.list.d/mariadb.list /etc/apt/sources.list.d/mariadb.list
RUN apk add --no-cache mariadb-backup ca-certificates rsync socat
RUN useradd -m -u 65532 -s /usr/sbin/nologin php84-mysql 2>/dev/null || true
RUN mkdir -p /var/lib/php84-mysql /var/log/php84-mysql /var/cache/php84-mysql /run/mysqld /etc/galera
RUN chown -R 65532:65532 /var/lib/php84-mysql /var/log/php84-mysql /var/cache/php84-mysql /run/mysqld /etc/galera
USER 65532:65532
WORKDIR /var/lib/php84-mysql
EXPOSE 3306 4567 4568 4444
ENTRYPOINT ["mariadbd", "--wsrep_new_cluster"]
LABEL org.opencontainers.image.title="mariadb-galera" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened MariaDB Galera - multi-master cluster" \
      org.opencontainers.image.vendor="MariaDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM