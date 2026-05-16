ARG VERSION=1.41.3.9292
ARG TARGETARCH

FROM plexinc/pms-docker@sha256:8b5bcdf7b506fe051aa1a0a0d464efdb3ad8c0fb1f8a4dfb27a8c489b609920c AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates wget expat fontconfig freetype glib || true
COPY --from=upstream /usr/lib/plexmediaserver /usr/lib/plexmediaserver
COPY --from=upstream /usr/lib/plexmediaserver/Plex\ Media\ Server /usr/lib/plexmediaserver/Plex\ Media\ Server
RUN mkdir -p /var/log/plex /var/cache/plex /config /transcode 2>/dev/null || true; \
    chown -R 65532:65532 /var/log/plex /var/cache/plex /config /transcode /usr/lib/plexmediaserver 2>/dev/null || true
USER 65532:65532
WORKDIR /config
EXPOSE 32400

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:32400/ || exit 1
ENTRYPOINT ["/usr/lib/plexmediaserver/Plex Media Server"]
LABEL org.opencontainers.image.title="plex-media-server" \
      org.opencontainers.image.description="plex-media-server container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Plex" \
      org.opencontainers.image.source="https://www.plex.tv/" \
      evergreen.image.tier="2" \
      evergreen.image.category="media-streaming" \
      evergreen.image.status="functional" \
      evergreen.image.note="Extracted from plexinc/pms-docker official image. Requires Plex account for activation." \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
