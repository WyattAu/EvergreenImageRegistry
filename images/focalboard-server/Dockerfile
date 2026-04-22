ARG VERSION=7.11.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mattermost/focalboard/releases/download/v{version}/focalboard-server-linux-amd64.tar.gz" -o /focalboard.tar.gz && \
    tar -xzf /focalboard.tar.gz -C /opt/ && rm /focalboard.tar.gz

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/focalboard /opt/focalboard
RUN mkdir -p /app /var/log/focalboard /var/cache/focalboard /data \
    && chown -R 65534:65534 /app /var/log/focalboard /var/cache/focalboard /data /opt/focalboard
USER 65534:65534
WORKDIR /data
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8000/api/v2/health"]
ENTRYPOINT ["/opt/focalboard/bin/focalboard-server"]
LABEL org.opencontainers.image.title="focalboard-server" \
      org.opencontainers.image.version="7.11.3" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/focalboard" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
