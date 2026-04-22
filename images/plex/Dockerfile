ARG VERSION=1.41.3.9292
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates xz-utils && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://downloads.plex.tv/plex-media-server-new/1.41.3.9292-f5fc49b19/debian/plexmediaserver_1.41.3.9292-f5fc49b19_amd64.deb" -o /plex.deb

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl libexpat1 libfontconfig1 libfreetype6 \
        libglib2.0-0 libx11-6 libxcb1 libxdamage1 libxext6 \
        libxfixes3 libxrender1 libxss1 libxtst6 && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /plex.deb /tmp/plex.deb
RUN dpkg -i /tmp/plex.deb && rm /tmp/plex.deb
RUN mkdir -p /var/log/plex /var/cache/plex /config /transcode \
    && chown -R 65534:65534 /var/log/plex /var/cache/plex /config /transcode /usr/lib/plexmediaserver
USER 65534:65534
WORKDIR /config
EXPOSE 32400
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:32400/identity"]
ENTRYPOINT ["/usr/lib/plexmediaserver/Plex Media Server"]
LABEL org.opencontainers.image.title="plex" \
      org.opencontainers.image.version="1.41.3.9292" \
      org.opencontainers.image.vendor="Plex" \
      org.opencontainers.image.source="https://www.plex.tv/" \
      sovereign.image.tier="2" \
      sovereign.image.category="media-streaming" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
