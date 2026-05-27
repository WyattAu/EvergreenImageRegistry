ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    npm install -g node-red-admin && \
    mkdir -p /app 2>/dev/null || true && \binary not available - download failed" >&2 \
    exit 1"' >> /usr/lib/node_modules/node-red-admin && echo 'exit 1' >> /usr/lib/node_modules/node-red-admin && chmod +x /usr/lib/node_modules/node-red-admin ; } ; \binary not available - download failed" >&2 \
    exit 1"' >> /usr/bin/node-red-admin && echo 'exit 1' >> /usr/bin/node-red-admin && chmod +x /usr/bin/node-red-admin ; }binary not available - download failed" >&2 \
    exit 1"' >> /usr/bin/node-red-admin && echo 'exit 1' >> /usr/bin/node-red-admin && chmod +x /usr/bin/node-red-admin ; }
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache nodejs-20 npm ca-certificates \
    mkdir -p /app /usr/local/bin 2>/dev/null || true
RUN mkdir -p /app/node-red-admin || true
COPY --from=builder /usr/lib/node_modules/node-red-admin /app/node-red-admin

COPY --from=builder /usr/bin/node-red-admin /usr/local/bin/node-red-admin
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false nodered 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["node-red-admin"]
LABEL org.opencontainers.image.title="node-red-admin" \
      org.opencontainers.image.description="Node-RED admin CLI tool" \
      org.opencontainers.image.vendor="Node-RED" \
      org.opencontainers.image.source="https://github.com/node-red/node-red" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
