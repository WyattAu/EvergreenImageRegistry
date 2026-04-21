# =============================================================================
# SOVEREIGN HARDENED MARIADB-10
# Constraint: debian-slim - native database package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.11.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg2 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://mariadb.org/mariadb_release_signing_key.asc" | gpg --dearmor -o /usr/share/keyrings/mariadb-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/mariadb-keyring.gpg] http://mirror.mariadb.org/repo/10.11/debian bookworm main" > /etc/apt/sources.list.d/mariadb.list

FROM debian:bookworm-slim
COPY --from=builder /usr/share/keyrings/mariadb-keyring.gpg /usr/share/keyrings/mariadb-keyring.gpg
COPY --from=builder /etc/apt/sources.list.d/mariadb.list /etc/apt/sources.list.d/mariadb.list
RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-server ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin mysql 2>/dev/null || true
RUN mkdir -p /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld
RUN chown -R 65534:65534 /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld
USER 65534:65534
WORKDIR /var/lib/mysql
EXPOSE 3306
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["mariadb-admin", "ping", "-h", "127.0.0.1", "--silent"]
ENTRYPOINT ["mariadbd"]
LABEL org.opencontainers.image.title="mariadb-10" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened MariaDB 10.x - LTS SQL database" \
      org.opencontainers.image.vendor="MariaDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
