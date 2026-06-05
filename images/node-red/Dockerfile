
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ ; rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone -b 3.1.0 https://github.com/node-red/node-red.git /src || { echo "Binary not available - download failed" >&2; exit 1; } && \
    mkdir -p /src 2>/dev/null || true && \
    cd /src && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null --omit=dev && npm run build 2>/dev/null && \
    mkdir -p /app /data 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache nodejs-20 npm ca-certificates
COPY --from=builder /src /app/src
COPY --from=builder /data /data
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /data -s /bin/false nodered 2>/dev/null || true && \
    chown -R 65532:65532 /app /data 2>/dev/null || true
USER 65532:65532
WORKDIR /data
EXPOSE 1880

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:1880"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "node", "--", "--userDir", "/data"]
LABEL org.opencontainers.image.title="node-red" \
      org.opencontainers.image.description="Node-RED - Flow-based programming for IoT" \
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
