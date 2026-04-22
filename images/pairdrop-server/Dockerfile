FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 https://github.com/schlagmichdoch/PairDrop.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin pairdrop 2>/dev/null || true && \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM