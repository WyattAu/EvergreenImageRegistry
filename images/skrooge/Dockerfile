ARG VERSION=2.31.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        skrooge \
        ca-certificates curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/app /var/cache/app \
    && chown -R 65534:65534 /app /var/log/app /var/cache/app
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8080"] 2>/dev/null || ["true"]
ENTRYPOINT ["skrooge"]
LABEL org.opencontainers.image.title="skrooge" \
      org.opencontainers.image.version="2.31.0" \
      org.opencontainers.image.vendor="Skrooge" \
      org.opencontainers.image.source="https://github.com/skrooge/skrooge" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
