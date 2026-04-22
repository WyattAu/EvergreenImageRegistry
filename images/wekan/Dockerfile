ARG VERSION=7.18.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/wekan/wekan/releases/download/v7.18.0/wekan-7.18.0-amd64.tar.gz" -o /wekan.tar.gz && \
    tar -xzf /wekan.tar.gz -C /opt/ && rm /wekan.tar.gz

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/bundle /opt/wekan
RUN mkdir -p /app /var/log/wekan /var/cache/wekan \
    && chown -R 65534:65534 /app /var/log/wekan /var/cache/wekan /opt/wekan
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8080"]
ENTRYPOINT ["node", "/opt/wekan/main.js"]
LABEL org.opencontainers.image.title="wekan" \
      org.opencontainers.image.version="7.18.0" \
      org.opencontainers.image.vendor="Wekan" \
      org.opencontainers.image.source="https://github.com/wekan/wekan" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
