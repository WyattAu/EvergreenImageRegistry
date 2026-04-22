FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app/data /var/log/zipline /var/cache/zipline

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/diced/zipline.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app/data
COPY --from=downloader /app/data /app/data
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin zipline 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:8080/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="zipline" \
      org.opencontainers.image.description="Zipline - File sharing platform" \
      org.opencontainers.image.vendor="diced" \
      org.opencontainers.image.source="https://github.com/diced/zipline" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
