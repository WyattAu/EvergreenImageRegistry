ARG VERSION=4.9.0.30
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/MediaBrowser/Emby.Releases/releases/download/4.9.0.30/emby-server-debian_4.9.0.30_amd64.deb" -o /emby.deb

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl libfontconfig1 libfreetype6 \
        libglib2.0-0 libice6 libsm6 libx11-6 libxext6 \
        libxrender1 && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /emby.deb /tmp/emby.deb
RUN dpkg -i /tmp/emby.deb && rm /tmp/emby.deb
RUN mkdir -p /var/log/emby /var/cache/emby /config \
    && chown -R 65534:65534 /var/log/emby /var/cache/emby /config /opt/emby-server
USER 65534:65534
WORKDIR /config
EXPOSE 8096 8920
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8096/emby/System/Info/Public"]
ENTRYPOINT ["/opt/emby-server/emby-server"]
LABEL org.opencontainers.image.title="emby" \
      org.opencontainers.image.version="4.9.0.30" \
      org.opencontainers.image.vendor="Emby" \
      org.opencontainers.image.source="https://github.com/MediaBrowser/Emby" \
      sovereign.image.tier="2" \
      sovereign.image.category="media-streaming" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
