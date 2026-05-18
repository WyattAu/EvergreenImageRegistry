ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app-data /var/log/node /var/cache/node 2>/dev/null || true && \
    mkdir -p /app 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache nodejs-20 ca-certificates curl 
COPY --from=builder /app /app
RUN mkdir -p /app /var/log/node /var/cache/node ; 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/node /var/cache/node
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="rclone-browser" \
      org.opencontainers.image.description="rclone-browser container image" \
      org.opencontainers.image.version="2.0.10" \
      org.opencontainers.image.vendor="Rclone Browser" \
      org.opencontainers.image.source="https://github.com/rclone/rclone-webui-react" \
      evergreen.image.tier="2" \
      evergreen.image.category="cloud-storage" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
