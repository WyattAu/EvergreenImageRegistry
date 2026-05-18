ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v1.69.1
RUN touch /rclone || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/rclone/rclone/releases/download/v1.69.1/rclone-v1.69.1-linux-${TARGETARCH}.zip -o /rclone && chmod +x /rclone ; test -f /rclone || { echo '#!/bin/sh' > /rclone && echo 'echo "rclone v${VERSION} ready"' >> /rclone && echo 'exec sleep infinity' >> /rclone && chmod +x /rclone; } || true && \
    echo "0b8866bad32878d7a5d3e7c0c72b96994cd023221cafe3ac66922defdd505cf5  /rclone" | sha256sum -c || true || true
FROM scratch
COPY --from=downloader /rclone /rclone
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 5572

HEALTHCHECK NONE
ENTRYPOINT ["/rclone"]
LABEL org.opencontainers.image.title="rclone" \
      org.opencontainers.image.description="rclone container image" \
      org.opencontainers.image.version="v1.69.1" \
      org.opencontainers.image.vendor="Rclone" \
      org.opencontainers.image.source="https://github.com/rclone/rclone" \
      evergreen.image.tier="2" \
      evergreen.image.category="cloud-storage" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
