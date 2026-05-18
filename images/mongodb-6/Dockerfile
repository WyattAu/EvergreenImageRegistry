# =============================================================================
# EVERGREEN HARDENED MONGODB-6
# Generated from template - Version: 6.0.14
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=6.0.14
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN useradd -m -u 65532 -s /usr/bin/false mongodb 2>/dev/null || true && \
    mkdir -p /app /var/log/mongod /var/cache/mongod 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/mongod /var/log/mongod
COPY --from=builder --chown=65532:65532 /var/cache/mongod /var/cache/mongod
USER 65532:65532
WORKDIR /app
EXPOSE 27017

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD echo "db.runCommand({ping:1})" | mongosh --quiet
ENTRYPOINT ["mongod"]
LABEL org.opencontainers.image.title="mongodb-6" \
      org.opencontainers.image.description="mongodb-6 container image" \
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
