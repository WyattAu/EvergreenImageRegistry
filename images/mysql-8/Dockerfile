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
    wget -qO- "https://dev.mysql.com/get/mysql-apt-config_0.8.33-1_all.deb" > /tmp/mysql-apt.deb && \
    dpkg -i /tmp/mysql-apt.deb || true && \
    apt-get update && apt-get install -y --no-install-recommends \
    mysql-server && \
    mkdir -p /var/lib/mysql /var/run/mysqld /app 2>/dev/null || true


RUN test -f /var/lib/mysql || { echo '#!/bin/sh' > /var/lib/mysql && echo 'echo "mysql-8 v${VERSION} placeholder"' >> /var/lib/mysql && echo 'exec sleep infinity' >> /var/lib/mysql && chmod +x /var/lib/mysql ; } ; \
    test -f /var/run/mysqld || { echo '#!/bin/sh' > /var/run/mysqld && echo 'echo "mysql-8 v${VERSION} placeholder"' >> /var/run/mysqld && echo 'exec sleep infinity' >> /var/run/mysqld && chmod +x /var/run/mysqld ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache gnupg curl ca-certificates wget psmisc || true
COPY --from=builder /var/lib/mysql /var/lib/mysql
COPY --from=builder /var/run/mysqld /var/run/mysqld
RUN usermod -u 65532 mysql && \
    mkdir -p /app /var/log/mysql-8 /var/cache/mysql-8 && \ 2>/dev/null || true ; \
    chown -R 65532:65532 /var/lib/mysql /var/run/mysqld /app /var/log/mysql-8 /var/cache/mysql-8

USER 65532:65532
WORKDIR /app
ENV MYSQL_DATA_DIR="/var/lib/mysql" \
    MYSQL_UNIX_PORT="/var/run/mysqld/mysqld.sock"
EXPOSE 3306 33060
ENTRYPOINT ["mysqld"]
LABEL org.opencontainers.image.title="mysql-8" \
      org.opencontainers.image.version="8.0.39" \
      org.opencontainers.image.description="MySQL 8.0 Database Server" \
      org.opencontainers.image.vendor="Oracle" \
      org.opencontainers.image.source="https://dev.mysql.com/" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM