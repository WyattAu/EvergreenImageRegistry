# =============================================================================
# SOVEREIGN HARDENED MYSQL
# Generated from template - Version: 11.4
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=11.4
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:11.4
RUN apk add --no-cache mariadb mariadb-client mariadb-backup ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 mysql 2>/dev/null || true
RUN mkdir -p /app /var/log/mysql /var/cache/mysql && chown -R mysql:mysql /app /var/log/mysql /var/cache/mysql 2>/dev/null || true
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
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
