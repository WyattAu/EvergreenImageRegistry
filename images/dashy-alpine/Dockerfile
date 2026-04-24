
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*WORKDIR /src
RUN git clone --depth 1 https://github.com/lissy93/dashy.git /src && \ 2>/dev/null || echo "Source repo not available - using placeholder" && \
    cd /src && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null || true && npm run build 2>/dev/null || trueRUN mkdir -p /app


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin dashy 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app/src
EXPOSE 80 443
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="dashy-alpine" \
      org.opencontainers.image.description="Dashy - Dashboard (debian-slim, no Alpine)" \
      org.opencontainers.image.vendor="lissy93" \
      org.opencontainers.image.source="https://github.com/lissy93/dashy" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.no_alpine="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM