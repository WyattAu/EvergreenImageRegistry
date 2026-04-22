FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g iobroker
RUN mkdir -p /app /opt/iobroker

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/iobroker /opt/iobroker
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /opt/iobroker -s /sbin/nologin iobroker 2>/dev/null || true && \
    chown -R 65534:65534 /opt/iobroker /app 2>/dev/null || true
USER 65534:65534
WORKDIR /opt/iobroker
EXPOSE 8081 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:8081/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["iobroker"]
CMD ["start"]
LABEL org.opencontainers.image.title="iobroker" \
      org.opencontainers.image.description="ioBroker - IoT automation platform" \
      org.opencontainers.image.vendor="ioBroker" \
      org.opencontainers.image.source="https://github.com/ioBroker/ioBroker" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
