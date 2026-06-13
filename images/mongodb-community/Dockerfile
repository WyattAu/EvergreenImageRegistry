# =============================================================================
# EVERGREEN HARDENED MONGODB-COMMUNITY
# Generated from template - Version: 7.0.9
# Wolfi-base provides glibc; binary installed from upstream deb packages
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.0.9
ARG BUILD_DATE
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG VERSION=7.0.9
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    ARCH=$(case ${TARGETARCH} in amd64) echo "x86_64" ;; arm64) echo "arm64" ;; *) echo "x86_64" ;; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL "https://fastdl.mongodb.org/linux/mongodb-linux-${ARCH}-ubuntu2204-${VERSION}.tgz" -o /tmp/mongodb.tgz ; echo "2cf223c0f901e0c6d218bdc7c607060b4155e273724e9d05babe10ce418c0391  /tmp/mongodb.tgz" | sha256sum -c  ; [ -f /tmp/mongodb.tgz ] && tar -xzf /tmp/mongodb.tgz -C /tmp ; \
    strip --strip-all /tmp/mongodb-linux-${ARCH}-ubuntu2204-${VERSION}/bin/* 2>/dev/null; mv /tmp/mongodb-linux-${ARCH}-ubuntu2204-${VERSION}/bin/* /usr/local/bin/ \
    && rm -rf /tmp/mongodb.tgz /tmp/mongodb-linux-${ARCH}-ubuntu2204-${VERSION} && { echo "Binary not available - download failed" >&2; exit 1; }
FROM ghcr.io/wyattau/evergreenshim/db-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=7.0.9

RUN apk add --no-cache ca-certificates && \
    addgroup -S -g 65532 mongodb && adduser -u 65532 -G mongodb -D -s /bin/false mongodb || true && \
    mkdir -p /data/db /var/log/mongodb /var/cache/mongodb && chown -R 65532:65532 /data/db /var/log/mongodb /var/cache/mongodb 2>/dev/null || true
COPY --from=builder /usr/local/bin/mongod /usr/local/bin/mongod
COPY --from=builder /usr/local/bin/mongos /usr/local/bin/mongos
COPY --from=builder /usr/local/bin/mongosh /usr/local/bin/mongosh
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="27017" \
    SHIM_BACKUP_SCHEDULE="0 0 2 * * *" \
    SHIM_BACKUP_RETENTION_DAYS="7" \
    SHIM_BACKUP_OUTPUT_DIR="/backups" \
    SHIM_REPLICATION_ENABLED="false" \
    SHIM_MIGRATION_ENABLED="false" \
    SHIM_VAULT_ENABLED="false" \
    SHIM_AUDIT_ENABLED="true" \
    SHIM_METRICS_ENABLED="true" \
    SHIM_ALERTING_ENABLED="false" \
    SHIM_ALERTING_WEBHOOK_URL="" \
    SHIM_SCHEDULER_ENABLED="true" \
    SHIM_SCHEDULER_BACKUP_CRON="0 0 2 * * *"
WORKDIR /data/db
EXPOSE 27017

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:27017"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="mongodb-community" \
      org.opencontainers.image.description="Evergreen hardened MongoDB Community Edition 7.0 - document database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MongoDB" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.edition="community" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/mongodb/mongo"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
