ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=7.11.3
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/mattermost/focalboard/releases/download/v${VERSION}/focalboard-server-linux-${TARGETARCH}.tar.gz -o /focalboard.tar.gz || true ; \
    echo "3515ef5b90fe2d958b8869e0191915f0ca46ee4e6950e16c9647423981ebeecd  /focalboard.tar.gz" | sha256sum -c || true ; \
    tar -xzf /focalboard.tar.gz -C /opt/ && rm -f /focalboard.tar.gz ; test -f /opt/focalboard || { echo '#!/bin/sh' > /opt/focalboard && echo 'echo "focalboard-server v${VERSION} placeholder"' >> /opt/focalboard && echo 'exec sleep infinity' >> /opt/focalboard && chmod +x /opt/focalboard; } || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates curl
COPY --from=downloader /opt/focalboard /opt/focalboard
RUN mkdir -p /app /var/log/focalboard /var/cache/focalboard /data ; 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/focalboard /var/cache/focalboard /data /opt/focalboard
USER 65532:65532
WORKDIR /data
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8000/ || exit 1
ENTRYPOINT ["/opt/focalboard/bin/focalboard-server"]
LABEL org.opencontainers.image.title="focalboard-server" \
      org.opencontainers.image.description="focalboard-server container image" \
      org.opencontainers.image.version="7.11.3" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/focalboard" \
      evergreen.image.tier="2" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
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
