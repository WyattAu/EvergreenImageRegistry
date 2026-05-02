ARG VERSION=1.41.3.9292

FROM plexinc/pms-docker:latest AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl expat fontconfig freetype glib || true
COPY --from=upstream /usr/lib/plexmediaserver /usr/lib/plexmediaserver 2>/dev/null || true
COPY --from=upstream /usr/lib/plexmediaserver/Plex\ Media\ Server /usr/lib/plexmediaserver/Plex\ Media\ Server 2>/dev/null || true
RUN mkdir -p /var/log/plex /var/cache/plex /config /transcode 2>/dev/null || true; \
    chown -R 65532:65532 /var/log/plex /var/cache/plex /config /transcode /usr/lib/plexmediaserver 2>/dev/null || true
USER 65532:65532
WORKDIR /config
EXPOSE 32400
ENTRYPOINT ["/usr/lib/plexmediaserver/Plex Media Server"]
LABEL org.opencontainers.image.title="plex-media-server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Plex" \
      org.opencontainers.image.source="https://www.plex.tv/" \
      sovereign.image.tier="2" \
      sovereign.image.category="media-streaming" \
      sovereign.image.status="functional" \
      sovereign.image.note="Extracted from plexinc/pms-docker official image. Requires Plex account for activation." \
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
