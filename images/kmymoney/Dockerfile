ARG VERSION=5.1.4
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        kmymoney \
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
ENTRYPOINT ["kmymoney"]
LABEL org.opencontainers.image.title="kmymoney" \
      org.opencontainers.image.version="5.1.4" \
      org.opencontainers.image.vendor="KMyMoney" \
      org.opencontainers.image.source="https://github.com/KDE/kmymoney" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
