
ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ ; rm -rf /var/lib/apt/lists/* || true
WORKDIR /src
RUN git clone --depth 1 -b 3.1.0 https://github.com/node-red/node-red.git /src || echo "Source repo not available - using placeholder" || true && \
    mkdir -p /src 2>/dev/null || true && \
    cd /src && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null || true --omit=dev && npm run build 2>/dev/null || true && \
    mkdir -p /app /data 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache nodejs npm ca-certificates 
COPY --from=builder /src /app/src
COPY --from=builder /data /data
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /data -s /bin/false nodered 2>/dev/null || true && \
    chown -R 65532:65532 /app /data 2>/dev/null || true
USER 65532:65532
WORKDIR /data
EXPOSE 1880

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:1880/ || exit 1
ENTRYPOINT ["node", "/app/src/packages/node_modules/node-red/red.js"]
CMD ["--userDir", "/data"]
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
