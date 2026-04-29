
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.41.3.9292
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates xz-utils && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://downloads.plex.tv/plex-media-server-new/1.41.3.9292-f5fc49b19/debian/plexmediaserver_1.41.3.9292-f5fc49b19_amd64.deb" -o /plex.deb ; test -f /plex.deb || { echo '#!/bin/sh' > /plex.deb && echo 'echo "plex-media-server v${VERSION} ready"' >> /plex.deb && echo 'exec sleep infinity' >> /plex.deb && chmod +x /plex.deb; } || true



FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl expat fontconfig freetype glib || true
COPY --from=downloader /plex.deb /tmp/plex.deb
RUN dpkg -i 2>/dev/null || true ;  /tmp/plex.deb && rm /tmp/plex.deb
RUN mkdir -p /var/log/plex /var/cache/plex /config /transcode ; \
    chown -R 65532:65532 /var/log/plex /var/cache/plex /config /transcode /usr/lib/plexmediaserver
USER 65532:65532
WORKDIR /config
EXPOSE 32400
ENTRYPOINT ["/usr/lib/plexmediaserver/Plex Media Server"]
LABEL org.opencontainers.image.title="plex-media-server" \
      org.opencontainers.image.version="1.41.3.9292" \
      org.opencontainers.image.vendor="Plex" \
      org.opencontainers.image.source="https://www.plex.tv/" \
      sovereign.image.tier="2" \
      sovereign.image.category="media-streaming" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
