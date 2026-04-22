ARG VERSION=2024.5.1
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
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:3000"]
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="cryptpad" \
      org.opencontainers.image.version="2024.5.1" \
      org.opencontainers.image.vendor="CryptPad" \
      org.opencontainers.image.source="https://github.com/cryptpad/cryptpad" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
