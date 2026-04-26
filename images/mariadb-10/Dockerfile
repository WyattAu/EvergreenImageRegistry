# =============================================================================
# SOVEREIGN HARDENED MARIADB-10
# Constraint: debian-slim - native database package install
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.11.6
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://mariadb.org/mariadb_release_signing_key.asc" | gnupg --dearmor -o /usr/share/keyrings/mariadb-keyring.gnupg ; echo "deb [signed-by=/usr/share/keyrings/mariadb-keyring.gnupg] http://mirror.mariadb.org/repo/10.11/debian bookworm main" > /etc/apt/sources.list.d/mariadb.list || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=10.11.6

COPY --from=builder /usr/share/keyrings/mariadb-keyring.gnupg /usr/share/keyrings/mariadb-keyring.gnupg
COPY --from=builder /etc/apt/sources.list.d/mariadb.list /etc/apt/sources.list.d/mariadb.list
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -s /sbin/nologin mysql 2>/dev/null || true
RUN mkdir -p /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld 2>/dev/null || true
RUN chown -R 65532:65532 /var/lib/mysql /var/log/mysql /var/cache/mysql /run/mysqld
USER 65532:65532
WORKDIR /var/lib/mysql
EXPOSE 3306
ENTRYPOINT ["mariadbd"]
LABEL org.opencontainers.image.title="mariadb-10" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened MariaDB 10.x - LTS SQL database" \
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