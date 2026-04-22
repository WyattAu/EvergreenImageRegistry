FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /src && \
    npm ci --omit=dev && npm run build 2>/dev/null || true
RUN mkdir -p /app /data

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=builder /src /app/src
COPY --from=builder /data /data
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin zigbee2mqtt 2>/dev/null || true && \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM