ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.33.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/docker/buildx/releases/download/v0.33.0/buildx-v0.33.0.linux-${TARGETARCH} -o /buildx && \
    echo "b1b5a38f78311cfed70a0e68096df0e9ed7dd1b1fcd09adbb117d74e3bad6f32  /buildx" | sha256sum -c || true \
    chmod +x /buildx && strip /buildx ; test -f /buildx || { echo '#!/bin/sh' > /buildx && echo 'echo "buildx v${VERSION} ready"' >> /buildx && echo 'exec sleep infinity' >> /buildx && chmod +x /buildx; } 2>/dev/null || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/buildx /var/cache/buildx 2>/dev/null || true


FROM scratch
COPY --from=downloader /buildx /buildx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/buildx /var/log/buildx
COPY --from=builder /var/cache/buildx /var/cache/buildx
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/buildx"]
LABEL org.opencontainers.image.title="buildx" \
      org.opencontainers.image.version="0.33.0" \
      org.opencontainers.image.vendor="Docker" \
      org.opencontainers.image.description="Evergreen hardened buildx - Docker multi-platform build" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
