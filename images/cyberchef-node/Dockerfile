FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch v10.5.0 https://github.com/gchq/CyberChef.git /src && \
    cd /src && npm ci && npm run build:node 2>/dev/null || npm run build
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache nodejs npm ca-certificates
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin cyberchef 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app/src
EXPOSE 3000
ENTRYPOINT ["node", "CyberChef.js"]
LABEL org.opencontainers.image.title="cyberchef-node" \
      org.opencontainers.image.description="CyberChef - Node.js variant" \
      org.opencontainers.image.vendor="GCHQ" \
      org.opencontainers.image.source="https://github.com/gchq/CyberChef" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM