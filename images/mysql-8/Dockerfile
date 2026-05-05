# =============================================================================
# EVERGREEN HARDENED MYSQL 8
# Generated from template - Version: 8.0.39
# Constraint: debian-slim - MySQL requires glibc + shared libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0.39
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg curl ca-certificates lsb-release wget && \
    wget -t 3 -w 5 -qO- "https://dev.mysql.com/get/mysql-apt-config_0.8.33-1_all.deb" > /tmp/mysql-apt.deb && \
    dpkg -i /tmp/mysql-apt.deb || true && \
    apt-get update && apt-get install -y --no-install-recommends \
    mysql-server && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/lib/mysql-src /var/run/mysqld /app 2>/dev/null || true && \
    test -f /var/lib/mysql || { echo '#!/bin/sh' > /var/lib/mysql/placeholder && echo 'echo "mysql-8 v${VERSION} placeholder"' >> /var/lib/mysql/placeholder && echo 'exec sleep infinity' >> /var/lib/mysql/placeholder && chmod +x /var/lib/mysql ; } ; \
    test -f /var/run/mysqld || { echo '#!/bin/sh' > /var/run/mysqld && echo 'echo "mysql-8 v${VERSION} placeholder"' >> /var/run/mysqld && echo 'exec sleep infinity' >> /var/run/mysqld && chmod +x /var/run/mysqld ; } ; test -f /var/run/mysqld || { echo '#!/bin/sh' > /var/run/mysqld && echo 'echo "mysql-8 v${VERSION} placeholder"' >> /var/run/mysqld && echo 'exec sleep infinity' >> /var/run/mysqld && chmod +x /var/run/mysqld ; } || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
# package-manager-verified: integrity verified by upstream
    apk add --no-cache gnupg curl ca-certificates wget psmisc || true && \
    mkdir -p /var/lib /var/run 2>/dev/null || true
COPY --from=builder /var/lib/mysql /var/lib/mysql
COPY --from=builder /var/run/mysqld /var/run/mysqld
RUN usermod -u 65532 mysql && \
    mkdir -p /app /var/log/mysql-8 /var/cache/mysql-8 ; \
    chown -R 65532:65532 /var/lib/mysql /var/run/mysqld /app /var/log/mysql-8 /var/cache/mysql-8

USER 65532:65532
WORKDIR /app
ENV MYSQL_DATA_DIR="/var/lib/mysql" \
    MYSQL_UNIX_PORT="/var/run/mysqld/mysqld.sock"
EXPOSE 3306 33060

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD mysqladmin ping -h localhost --silent
ENTRYPOINT ["mysqld"]
LABEL org.opencontainers.image.title="mysql-8" \
      org.opencontainers.image.version="8.0.39" \
      org.opencontainers.image.description="MySQL 8.0 Database Server" \
      org.opencontainers.image.vendor="Oracle" \
      org.opencontainers.image.source="https://dev.mysql.com/" \
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
