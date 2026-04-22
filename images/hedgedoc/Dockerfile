FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends         nodejs npm git ca-certificates python3 make g++     && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch master https://github.com/hedgedoc/hedgedoc.git /src &&     cd /src && npm ci && npm run build
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends         nodejs npm ca-certificates     && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin hedgedoc 2>/dev/null || true &&     chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app/src
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3     CMD ["node", "-e", "require('http').get('http://localhost:3000/', (r) => { if (r.statusCode !== 200) process.exit(1) }).on('error', () => process.exit(1))"] || exit 0
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="hedgedoc"       org.opencontainers.image.description="HedgeDoc - Collaborative markdown notes"       org.opencontainers.image.vendor="HedgeDoc"       org.opencontainers.image.source="https://github.com/hedgedoc/hedgedoc"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
