FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /src && \
    npm ci --omit=dev && npm run build 2>/dev/null || true
RUN mkdir -p /app /data

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /data /data
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin zigbee2mqtt 2>/dev/null || true && \
    chown -R 65534:65534 /app /data 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:8080/api/info', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"]
ENTRYPOINT ["node", "index.js"]
LABEL org.opencontainers.image.title="zigbee2mqtt" \
      org.opencontainers.image.description="Zigbee to MQTT bridge" \
      org.opencontainers.image.vendor="Koenkk" \
      org.opencontainers.image.source="https://github.com/Koenkk/zigbee2mqtt" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
