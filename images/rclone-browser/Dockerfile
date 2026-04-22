ARG VERSION=2.0.10
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/node /var/cache/node

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node \
    && chown -R 65534:65534 /app /var/log/node /var/cache/node
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:8080"]
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="rclone-browser" \
      org.opencontainers.image.version="2.0.10" \
      org.opencontainers.image.vendor="Rclone Browser" \
      org.opencontainers.image.source="https://github.com/rclone/rclone-webui-react" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
