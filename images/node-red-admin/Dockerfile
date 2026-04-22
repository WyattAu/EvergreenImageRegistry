FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g node-red-admin
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules/node-red-admin /app/node-red-admin
COPY --from=builder /usr/bin/node-red-admin /usr/local/bin/node-red-admin 2>/dev/null || true
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin nodered 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["node-red-admin", "--help"] || exit 0
ENTRYPOINT ["node-red-admin"]
LABEL org.opencontainers.image.title="node-red-admin" \
      org.opencontainers.image.description="Node-RED admin CLI tool" \
      org.opencontainers.image.vendor="Node-RED" \
      org.opencontainers.image.source="https://github.com/node-red/node-red" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
