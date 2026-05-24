# =============================================================================
# EVERGREEN HARDENED MONGODB-6
# Uses official mongo image as upstream binary source on Wolfi base
# =============================================================================

ARG VERSION=6.0.14
ARG TARGETARCH

FROM mongo:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ENV EVERGREEN_LOG_LEVEL=info

RUN apk add --no-cache ca-certificates

COPY --from=upstream /usr/bin/mongod /usr/bin/mongod
COPY --from=upstream /usr/bin/mongos /usr/bin/mongos
COPY --from=upstream /usr/bin/mongosh /usr/bin/mongosh

RUN adduser -D -u 65532 -s /bin/false mongodb 2>/dev/null || true && \
    mkdir -p /app /var/log/mongod /var/cache/mongod /data/db && \
    chown -R 65532:65532 /app /var/log/mongod /var/cache/mongod /data/db

USER 65532:65532
WORKDIR /app
EXPOSE 27017

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD echo "db.runCommand({ping:1})" | mongosh --quiet
ENTRYPOINT ["mongod"]
CMD ["--bind_ip", "0.0.0.0", "--dbpath", "/data/db"]
LABEL org.opencontainers.image.title="mongodb-6" \
      org.opencontainers.image.description="MongoDB 6 - document-oriented NoSQL database" \
      org.opencontainers.image.version="6.0.14" \
      org.opencontainers.image.vendor="MongoDB" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      org.opencontainers.image.source="https://github.com/mongodb/mongo"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
