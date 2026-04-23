FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch v2024.3.21 https://github.com/CorentinTh/it-tools.git /src && \
    cd /src && npm ci && npm run build
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN adduser -u 65532 -G nogroup -D -h /app -s /sbin/nologin ittools 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app/src
EXPOSE 8080
ENTRYPOINT ["node", "server.js"]
LABEL org.opencontainers.image.title="it-tools-legacy" \
      org.opencontainers.image.description="IT Tools - legacy version (debian-slim, no Alpine)" \
      org.opencontainers.image.vendor="CorentinTh" \
      org.opencontainers.image.source="https://github.com/CorentinTh/it-tools" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.no_alpine="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM