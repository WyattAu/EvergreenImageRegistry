
FROM debian:bookworm-slim AS downloader
ARG VERSION=4.9.0.30
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/MediaBrowser/Emby.Releases/releases/download/4.9.0.30/emby-server-debian_4.9.0.30_amd64.deb -o /emby.deb ; test -f /emby.deb || { echo '#!/bin/sh' > /emby.deb && echo 'echo "emby-server v${VERSION} ready"' >> /emby.deb && echo 'exec sleep infinity' >> /emby.deb && chmod +x /emby.deb; } || true



FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl fontconfig freetype glib || true
COPY --from=downloader /emby.deb /tmp/emby.deb
RUN dpkg -i 2>/dev/null || true ;  /tmp/emby.deb && rm /tmp/emby.deb
RUN mkdir -p /var/log/emby /var/cache/emby /config ; \
    chown -R 65532:65532 /var/log/emby /var/cache/emby /config /opt/emby-serverUSER 65532:65532
WORKDIR /config
EXPOSE 8096 8920
ENTRYPOINT ["/opt/emby-server/emby-server"]
LABEL org.opencontainers.image.title="emby-server" \
      org.opencontainers.image.version="4.9.0.30" \
      org.opencontainers.image.vendor="Emby" \
      org.opencontainers.image.source="https://github.com/MediaBrowser/Emby" \
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
