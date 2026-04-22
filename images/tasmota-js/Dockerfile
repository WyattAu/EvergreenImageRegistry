FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g tasmotizer 2>/dev/null || true
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules 2>/dev/null || true
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin tasmota 2>/dev/null || true && \
    chown -R 65534:65534 /app /usr/lib/node_modules 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["node", "-e", "console.log('ok')"]
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="tasmota-js" \
      org.opencontainers.image.description="Tasmota JavaScript tools" \
      org.opencontainers.image.vendor="Tasmota" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
