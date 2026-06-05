# =============================================================================
# EVERGREEN HARDENED MYSQL
# Uses official mysql image as upstream binary source on Wolfi base
# =============================================================================

ARG VERSION=8.4.1
ARG TARGETARCH

ARG SHIM_VERSION=v0.3.0

FROM mysql:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ENV HEALTH_CMD="mysqladmin ping -h 127.0.0.1 --silent" \
    READY_CMD="mysqladmin ping -h 127.0.0.1 --silent" \
    STARTUP_CMD="mysqladmin ping -h 127.0.0.1 --silent" \
    EVERGREEN_LOG_LEVEL=info

RUN apk add --no-cache ca-certificates

COPY --from=upstream /usr/sbin/mysqld /usr/sbin/mysqld
COPY --from=upstream /usr/bin/mysql /usr/bin/mysql
COPY --from=upstream /usr/bin/mysqladmin /usr/bin/mysqladmin
COPY --from=upstream /usr/bin/mysqldump /usr/bin/mysqldump
COPY --from=upstream /usr/lib/mysql/ /usr/lib/mysql/
COPY --from=upstream /usr/share/mysql/ /usr/share/mysql/

RUN adduser -D -u 65532 -s /bin/false mysql 2>/dev/null || true && \
    mkdir -p /app /var/log/mysql /var/cache/mysql /run/mysqld && \
    chown -R 65532:65532 /app /var/log/mysql /var/cache/mysql /run/mysqld

USER 65532:65532
ENV SHIM_BACKUP_ENABLED="false" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="5432" \
    SHIM_REPLICATION_ENABLED="false" \
    SHIM_MIGRATION_ENABLED="false" \
    SHIM_VAULT_ENABLED="false" \
    SHIM_AUDIT_ENABLED="true"
WORKDIR /app
EXPOSE 3306

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3306"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "mysqld", "--", "--user=mysql", "--datadir=/var/lib/mysql"]
LABEL org.opencontainers.image.title="mysql" \
      org.opencontainers.image.description="MySQL - open source relational database management system" \
      org.opencontainers.image.version="8.4.1" \
      org.opencontainers.image.vendor="Oracle" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      org.opencontainers.image.source="https://github.com/mysql/mysql-server"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
