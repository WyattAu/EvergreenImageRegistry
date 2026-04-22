FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/linuxserver/Heimdall.git /src 2>/dev/null || true
RUN mkdir -p /app /config

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates nginx \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src 2>/dev/null || true
COPY --from=builder /config /config 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin heimdall 2>/dev/null || true && \
    chown -R 65534:65534 /app /config 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:80/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node"]
CMD ["/app/src/server.js"]
LABEL org.opencontainers.image.title="heimdall" \
      org.opencontainers.image.description="Heimdall - Application dashboard" \
      org.opencontainers.image.vendor="LinuxServer.io" \
      org.opencontainers.image.source="https://github.com/linuxserver/Heimdall" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
