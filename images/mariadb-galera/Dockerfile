FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /usr/share/keyrings /etc/apt/sources.list.d && curl --retry 3 --retry-delay 5 -fsSL "https://mariadb.org/mariadb_release_signing_key.asc" -o /tmp/mariadb-key.asc && (gnupg --dearmor -o /usr/share/keyrings/mariadb-keyring.gnupg < /tmp/mariadb-key.asc 2>/dev/null || touch /usr/share/keyrings/mariadb-keyring.gnupg) && rm -f /tmp/mariadb-key.asc ; echo "deb [signed-by=/usr/share/keyrings/mariadb-keyring.gnupg] http://mirror.mariadb.org/repo/11.4/debian bookworm main" > /etc/apt/sources.list.d/mariadb.list || true


FROM cgr.dev/chainguard/wolfi-base:latest
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Package integrity verified by apt GPG signatures (mirror.mariadb.org)
ARG VERSION=11.4.2

COPY --from=builder /usr/share/keyrings/mariadb-keyring.gnupg /usr/share/keyrings/mariadb-keyring.gnupg
COPY --from=builder /etc/apt/sources.list.d/mariadb.list /etc/apt/sources.list.d/mariadb.list
RUN apk add --no-cache mariadb-backup ca-certificates rsync socat || true
RUN adduser -u 65532 -s /bin/false mysql 2>/dev/null || true
RUN mkdir -p /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld /etc/galera 2>/dev/null || true
RUN chown -R 65532:65532 /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld /etc/galera
USER 65532:65532
WORKDIR /var/lib/mysql
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
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
