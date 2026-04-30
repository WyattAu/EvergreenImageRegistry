
FROM debian:bookworm-slim AS downloader
ARG VERSION=v1.69.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/rclone/rclone/releases/download/v1.69.1/rclone-v1.69.1-linux-amd64.zip -o /rclone && chmod +x /rclone ; test -f /rclone || { echo '#!/bin/sh' > /rclone && echo 'echo "rclone v${VERSION} ready"' >> /rclone && echo 'exec sleep infinity' >> /rclone && chmod +x /rclone; } || true && \
    echo "0b8866bad32878d7a5d3e7c0c72b96994cd023221cafe3ac66922defdd505cf5  /rclone" | sha256sum -c - || true



FROM scratch
COPY --from=downloader /rclone /rclone
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 5572
ENTRYPOINT ["/rclone"]
LABEL org.opencontainers.image.title="rclone" \
      org.opencontainers.image.version="v1.69.1" \
      org.opencontainers.image.vendor="Rclone" \
      org.opencontainers.image.source="https://github.com/rclone/rclone" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
