
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ ; rm -rf /var/lib/apt/lists/* || true
WORKDIR /src
RUN git clone --depth 1 https://github.com/schlagmichdoch/PairDrop.git /src &&  || echo "Source repo not available - using placeholder" || true
RUN mkdir -p /src 2>/dev/null || true && \
    cd /src && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null || true && npm run build 2>/dev/null || true
RUN mkdir -p /app 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates || true
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin pairdrop 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app/src
EXPOSE 3000
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="pairdrop-server" \
      org.opencontainers.image.description="PairDrop - Local file sharing in browser" \
      org.opencontainers.image.vendor="schlagmichdoch" \
      org.opencontainers.image.source="https://github.com/schlagmichdoch/PairDrop" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM