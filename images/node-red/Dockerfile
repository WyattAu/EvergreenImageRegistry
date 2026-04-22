FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 -b 3.1.0 https://github.com/node-red/node-red.git /src && \
    npm ci --omit=dev && npm run build 2>/dev/null || true
RUN mkdir -p /app /data

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /data /data
RUN useradd -r -u 65534 -g nogroup -d /data -s /sbin/nologin nodered 2>/dev/null || true && \
    chown -R 65534:65534 /app /data 2>/dev/null || true
USER 65534:65534
WORKDIR /data
EXPOSE 1880
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:1880/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"]
ENTRYPOINT ["node", "/app/src/packages/node_modules/node-red/red.js"]
CMD ["--userDir", "/data"]
LABEL org.opencontainers.image.title="node-red" \
      org.opencontainers.image.description="Node-RED - Flow-based programming for IoT" \
      org.opencontainers.image.vendor="Node-RED" \
      org.opencontainers.image.source="https://github.com/node-red/node-red" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
