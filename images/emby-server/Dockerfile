FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=4.9.3.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/MediaBrowser/Emby.Releases/releases/download/${VERSION}/emby-server-deb_${VERSION}_amd64.deb" \
    -o /emby.deb && dpkg-deb -x /emby.deb /tmp/emby && rm -f /emby.deb

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates curl fontconfig freetype glib
COPY --from=downloader /tmp/emby/opt/emby-server /opt/emby-server
COPY --from=downloader /tmp/emby/var/log/emby /var/log/emby
COPY --from=downloader /tmp/emby/var/cache/emby /var/cache/emby
RUN mkdir -p /config && chown -R 65532:65532 /var/log/emby /var/cache/emby /config /opt/emby-server
USER 65532:65532
WORKDIR /config
EXPOSE 8096 8920

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8096/ || exit 1
ENTRYPOINT ["/opt/emby-server/emby-server"]
LABEL org.opencontainers.image.title="emby-server"       org.opencontainers.image.version="4.9.3.0"       org.opencontainers.image.vendor="Emby"       org.opencontainers.image.source="https://github.com/MediaBrowser/Emby.Releases"       evergreen.image.tier="2"       evergreen.image.category="media-streaming"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="wolfi"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="10s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
