FROM debian:bookworm-slim AS downloader
ARG VERSION=4.9.3.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/MediaBrowser/Emby.Releases/releases/download/${VERSION}/emby-server-deb_${VERSION}_amd64.deb" \
    -o /emby.deb && dpkg-deb -x /emby.deb /tmp/emby && rm -f /emby.deb

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates curl fontconfig freetype glib
COPY --from=downloader /tmp/emby/opt/emby-server /opt/emby-server
COPY --from=downloader /tmp/emby/var/log/emby /var/log/emby
COPY --from=downloader /tmp/emby/var/cache/emby /var/cache/emby
RUN mkdir -p /config && chown -R 65532:65532 /var/log/emby /var/cache/emby /config /opt/emby-server
USER 65532:65532
WORKDIR /config
EXPOSE 8096 8920
ENTRYPOINT ["/opt/emby-server/emby-server"]
LABEL org.opencontainers.image.title="emby-server"       org.opencontainers.image.version="4.9.3.0"       org.opencontainers.image.vendor="Emby"       org.opencontainers.image.source="https://github.com/MediaBrowser/Emby.Releases"       sovereign.image.tier="2"       sovereign.image.category="media-streaming"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="wolfi"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="10s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
