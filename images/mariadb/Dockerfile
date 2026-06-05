# =============================================================================
# EVERGREEN HARDENED MARIADB
# Uses official mariadb image as upstream binary source on Wolfi base
# =============================================================================

ARG VERSION=11.8
ARG TARGETARCH

ARG SHIM_VERSION=v0.2.0

FROM mariadb:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ENV HEALTH_CMD="mariadb-admin ping -h 127.0.0.1 --silent" \
    READY_CMD="mariadb-admin ping -h 127.0.0.1 --silent" \
    STARTUP_CMD="mariadb-admin ping -h 127.0.0.1 --silent" \
    EVERGREEN_LOG_LEVEL=info

RUN apk add --no-cache ca-certificates

COPY --from=upstream /usr/bin/mariadbd /usr/bin/mariadbd
COPY --from=upstream /usr/bin/mariadb-admin /usr/bin/mariadb-admin
COPY --from=upstream /usr/bin/mariadb /usr/bin/mariadb
COPY --from=upstream /usr/bin/mariadb-check /usr/bin/mariadb-check
COPY --from=upstream /usr/bin/mysqldump /usr/bin/mysqldump
COPY --from=upstream /usr/lib/mysql/ /usr/lib/mysql/
COPY --from=upstream /usr/share/mysql/ /usr/share/mysql/

RUN adduser -D -u 65532 -s /bin/false mysql 2>/dev/null || true && \
    mkdir -p /app /var/log/mariadbd /var/cache/mariadbd /run/mysqld && \
    chown -R 65532:65532 /app /var/log/mariadbd /var/cache/mariadbd /run/mysqld

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
CMD ["-c", "mariadbd", "--", "--user=mysql", "--datadir=/var/lib/mysql"]
LABEL org.opencontainers.image.title="mariadb" \
      org.opencontainers.image.description="MariaDB - community-developed fork of MySQL" \
      org.opencontainers.image.version="11.8" \
      org.opencontainers.image.vendor="MariaDB" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      org.opencontainers.image.source="https://github.com/MariaDB/server"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
