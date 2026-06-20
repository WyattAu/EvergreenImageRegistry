ARG VERSION=1.41.3.9292
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM plexinc/pms-docker:1.41.3.9292-bc7397402@sha256:a6060a5d0745806155190bfcf6f2fb4c4d7ac7e26984bca203e8ccaa857436ae AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates wget expat fontconfig freetype glib
RUN mkdir -p /usr/lib/plexmediaserver || true
COPY --from=upstream /usr/lib/plexmediaserver /usr/lib/plexmediaserver
RUN touch Media || true
COPY --from=upstream /usr/lib/plexmediaserver/Plex\ Media\ Server/ /usr/lib/plexmediaserver/Plex\ Media\ Server/
RUN mkdir -p /var/log/plex /var/cache/plex /config /transcode 2>/dev/null || true; \
    chown -R 65532:65532 /var/log/plex /var/cache/plex /config /transcode /usr/lib/plexmediaserver 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /config
EXPOSE 32400

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:32400"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/lib/plexmediaserver/Plex Media Server"]
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
