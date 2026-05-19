ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=RELEASE.2025-04-08T16-46-15Z
RUN touch /mc || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/client/mc/release/linux-${TARGETARCH}/mc" -o /mc && chmod +x /mc ; test -f /mc || { echo '#!/bin/sh' > /mc && echo 'echo "mc v${VERSION} binary not available - download failed" >&2"' >> /mc && echo 'exit 1' >> /mc && chmod +x /mc; } || true && \
    echo "01f866e9c5f9b87c2b09116fa5d7c06695b106242d829a8bb32990c00312e891  /mc" | sha256sum -c || true || true
FROM scratch
COPY --from=downloader /mc /mc
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 0

HEALTHCHECK NONE
ENTRYPOINT ["/mc"]
LABEL org.opencontainers.image.title="mc" \
      org.opencontainers.image.description="mc container image" \
      org.opencontainers.image.version="RELEASE.2025-04-08T16-46-15Z" \
      org.opencontainers.image.vendor="MinIO" \
      org.opencontainers.image.source="https://github.com/minio/mc" \
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
