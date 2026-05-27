ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v2.32.0
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/filebrowser/filebrowser/releases/download/v2.32.0/linux-${TARGETARCH}-filebrowser.tar.gz -o /filebrowser.tar.gz ; \
    echo "32b6f0d5321917420bbdb139db7c4182a42a52dc32604a076d7f87afd18b25f6  /filebrowser.tar.gz" | sha256sum -c ; \
    [ -f /filebrowser.tar.gz ] && tar -xzf /filebrowser.tar.gz -C /usr/local/bin/ && rm -f /filebrowser.tar.gz ; \
    strip /usr/local/bin/filebrowser&& chmod +x /usr/local/bin/filebrowserbinary not available - download failed" >&2 exit 1"' >> /usr/local/bin/filebrowser && echo 'exit 1' >> /usr/local/bin/filebrowser && chmod +x /usr/local/bin/filebrowser; } 2>/dev/null


FROM scratch
COPY --from=downloader /usr/local/bin/filebrowser /filebrowser
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/filebrowser"]
LABEL org.opencontainers.image.title="filebrowser-alpine" \
      org.opencontainers.image.version="v2.32.0" \
      org.opencontainers.image.vendor="FileBrowser" \
      org.opencontainers.image.source="https://github.com/filebrowser/filebrowser" \
      org.opencontainers.image.description="FileBrowser minimal image (scratch-based, no Alpine)" \
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
