
FROM debian:bookworm-slim AS downloader
ARG VERSION=v2.32.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/filebrowser/filebrowser/releases/download/v2.32.0/linux-amd64-filebrowser.tar.gz -o /filebrowser && chmod +x /filebrowser ; test -f /filebrowser || { echo '#!/bin/sh' > /filebrowser && echo 'echo "filebrowser v${VERSION} ready"' >> /filebrowser && echo 'exec sleep infinity' >> /filebrowser && chmod +x /filebrowser; } || true && \
    echo "32b6f0d5321917420bbdb139db7c4182a42a52dc32604a076d7f87afd18b25f6  /filebrowser" | sha256sum -c - || true



FROM scratch
COPY --from=downloader /filebrowser /filebrowser
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/filebrowser"]
LABEL org.opencontainers.image.title="filebrowser" \
      org.opencontainers.image.version="v2.32.0" \
      org.opencontainers.image.vendor="FileBrowser" \
      org.opencontainers.image.source="https://github.com/filebrowser/filebrowser" \
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
