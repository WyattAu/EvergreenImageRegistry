# =============================================================================
# SOVEREIGN HARDENED MARIADB-GALERA
# Constraint: debian-slim - native database + Galera cluster package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=11.4.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg2 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://mariadb.org/mariadb_release_signing_key.asc" | gpg --dearmor -o /usr/share/keyrings/mariadb-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/mariadb-keyring.gpg] http://mirror.mariadb.org/repo/11.4/debian bookworm main" > /etc/apt/sources.list.d/mariadb.list

FROM debian:bookworm-slim
COPY --from=builder /usr/share/keyrings/mariadb-keyring.gpg /usr/share/keyrings/mariadb-keyring.gpg
COPY --from=builder /etc/apt/sources.list.d/mariadb.list /etc/apt/sources.list.d/mariadb.list
RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-server galera-4 mariadb-backup ca-certificates rsync socat && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin mysql 2>/dev/null || true
RUN mkdir -p /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld /etc/galera
RUN chown -R 65534:65534 /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld /etc/galera
USER 65534:65534
WORKDIR /var/lib/mysql
EXPOSE 3306 4567 4568 4444
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["mariadb-admin", "ping", "-h", "127.0.0.1", "--silent"]
ENTRYPOINT ["mariadbd", "--wsrep_new_cluster"]
LABEL org.opencontainers.image.title="mariadb-galera" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened MariaDB Galera - multi-master cluster" \
      org.opencontainers.image.vendor="MariaDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
