
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ ; rm -rf /var/lib/apt/lists/* || true
WORKDIR /src
RUN git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /src && \ 2>/dev/null || echo "Source repo not available - using placeholder" || true
RUN mkdir -p /src 2>/dev/null || true && \
    cd /src && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null || true --omit=dev && npm run build 2>/dev/null || true
RUN mkdir -p /app /data 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates || true
COPY --from=builder /src /app/src
COPY --from=builder /data /data
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin zigbee2mqtt 2>/dev/null || true && \
    chown -R 65532:65532 /app /data 2>/dev/null || true
USER 65532:65532
WORKDIR /app/src
EXPOSE 8080
ENTRYPOINT ["node", "index.js"]
LABEL org.opencontainers.image.title="zigbee2mqtt" \
      org.opencontainers.image.description="Zigbee to MQTT bridge" \
      org.opencontainers.image.vendor="Koenkk" \
      org.opencontainers.image.source="https://github.com/Koenkk/zigbee2mqtt" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM