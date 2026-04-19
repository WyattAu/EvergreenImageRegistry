# =============================================================================
# SOVEREIGN HARDENED MYSQL
# Generated from template - Version: 11.4
# =============================================================================

ARG VERSION=11.4
ARG BUILD_DATE

FROM alpine:11.4-alpine
RUN apk add --no-cache mariadb mariadb-client mariadb-backup ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id mysql 2>/dev/null || adduser -D -u 65534 mysql
RUN mkdir -p /app /var/log/mysql /var/cache/mysql && chown -R mysql:mysql /app /var/log/mysql /var/cache/mysql
USER mysql:mysql
WORKDIR /app
EXPOSE 3306
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD mariadb-admin ping
ENTRYPOINT ["mariadbd"]
LABEL org.opencontainers.image.title="mysql" \
      org.opencontainers.image.version="11.4" \
      org.opencontainers.image.vendor="MariaDB" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
