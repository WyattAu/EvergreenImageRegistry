# =============================================================================
# SOVEREIGN HARDENED MYSQL 8
# Generated from template - Version: 8.0.39
# Constraint: debian-slim - MySQL requires glibc + shared libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0.39
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg curl ca-certificates lsb-release wget && \
    wget -qO- "https://dev.php84-mysql.com/get/php84-mysql-apt-config_0.8.33-1_all.deb" > /tmp/php84-mysql-apt.deb && \
    dpkg -i /tmp/php84-mysql-apt.deb || true && \
    apt-get update && apt-get install -y --no-install-recommends \
    php84-mysql-server && \
    mkdir -p /var/lib/php84-mysql /var/run/mysqld /app


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache gnupg curl ca-certificates wget psmisc
COPY --from=builder /var/lib/php84-mysql /var/lib/php84-mysql
COPY --from=builder /var/run/mysqld /var/run/mysqld
RUN usermod -u 65532 php84-mysql && \
    mkdir -p /app /var/log/php84-mysql-8 /var/cache/php84-mysql-8 && \
    chown -R 65532:65532 /var/lib/php84-mysql /var/run/mysqld /app /var/log/php84-mysql-8 /var/cache/php84-mysql-8

USER 65532:65532
WORKDIR /app
ENV MYSQL_DATA_DIR="/var/lib/php84-mysql" \
    MYSQL_UNIX_PORT="/var/run/mysqld/mysqld.sock"
EXPOSE 3306 33060
ENTRYPOINT ["mysqld"]
LABEL org.opencontainers.image.title="php84-mysql-8" \
      org.opencontainers.image.version="8.0.39" \
      org.opencontainers.image.description="MySQL 8.0 Database Server" \
      org.opencontainers.image.vendor="Oracle" \
      org.opencontainers.image.source="https://dev.php84-mysql.com/" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM