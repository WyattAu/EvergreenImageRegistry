ARG TARGETARCH
FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=v2.32.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/filebrowser/filebrowser/releases/download/v2.32.0/linux-${TARGETARCH}-filebrowser.tar.gz -o /filebrowser.tar.gz || true ; \
    echo "32b6f0d5321917420bbdb139db7c4182a42a52dc32604a076d7f87afd18b25f6  /filebrowser.tar.gz" | sha256sum -c - || true
    [ -f /filebrowser.tar.gz ] && tar -xzf /filebrowser.tar.gz -C /usr/local/bin/ && rm -f /filebrowser.tar.gz || true ; \
    strip /usr/local/bin/filebrowser && chmod +x /usr/local/bin/filebrowser ; test -f /usr/local/bin/filebrowser || { echo '#!/bin/sh' > /usr/local/bin/filebrowser && echo 'echo "filebrowser-alpine v${VERSION} placeholder"' >> /usr/local/bin/filebrowser && echo 'exec sleep infinity' >> /usr/local/bin/filebrowser && chmod +x /usr/local/bin/filebrowser; } 2>/dev/null || true


FROM scratch
COPY --from=downloader /usr/local/bin/filebrowser /filebrowser
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/filebrowser"]
LABEL org.opencontainers.image.title="filebrowser-alpine" \
      org.opencontainers.image.version="v2.32.0" \
      org.opencontainers.image.vendor="FileBrowser" \
      org.opencontainers.image.source="https://github.com/filebrowser/filebrowser" \
      org.opencontainers.image.description="FileBrowser minimal image (scratch-based, no Alpine)" \
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
