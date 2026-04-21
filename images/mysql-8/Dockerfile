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
    gnupg2 curl ca-certificates lsb-release wget && \
    wget -qO- "https://dev.mysql.com/get/mysql-apt-config_0.8.33-1_all.deb" > /tmp/mysql-apt.deb && \
    dpkg -i /tmp/mysql-apt.deb || true && \
    apt-get update && apt-get install -y --no-install-recommends \
    mysql-server && \
    mkdir -p /var/lib/mysql /var/run/mysqld /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates lsb-release wget \
    libaio1t64 libmecab2 libnuma1 psmisc && \
    wget -qO- "https://dev.mysql.com/get/mysql-apt-config_0.8.33-1_all.deb" > /tmp/mysql-apt.deb && \
    dpkg -i /tmp/mysql-apt.deb || true && \
    apt-get update && apt-get install -y --no-install-recommends \
    mysql-server && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /var/lib/mysql /var/lib/mysql
COPY --from=builder /var/run/mysqld /var/run/mysqld
RUN usermod -u 65534 mysql && \
    mkdir -p /app /var/log/mysql-8 /var/cache/mysql-8 && \
    chown -R 65534:65534 /var/lib/mysql /var/run/mysqld /app /var/log/mysql-8 /var/cache/mysql-8
USER 65534:65534
WORKDIR /app
ENV MYSQL_DATA_DIR="/var/lib/mysql" \
    MYSQL_UNIX_PORT="/var/run/mysqld/mysqld.sock"
EXPOSE 3306 33060
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["mysqladmin", "ping", "-h", "localhost"]
ENTRYPOINT ["mysqld"]
LABEL org.opencontainers.image.title="mysql-8" \
      org.opencontainers.image.version="8.0.39" \
      org.opencontainers.image.description="MySQL 8.0 Database Server" \
      org.opencontainers.image.vendor="Oracle" \
      org.opencontainers.image.source="https://dev.mysql.com/" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
