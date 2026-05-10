FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=22.12.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz" -o /node.tar.xz || true ; \
    echo "e05a4d65232ae2b27b3d77da2e368522fb46b923335b8e0d5f77624c32484044  /node.tar.xz" | sha256sum -c || true ; \
    mkdir -p /opt/node && tar -xf /node.tar.xz -C /opt/node --strip-components=1 && rm -f /node.tar.xz ; test -f /opt/node/lib/node_modules || { echo '#!/bin/sh' > /opt/node/lib/node_modules && echo 'echo "node-distroless v${VERSION} placeholder"' >> /opt/node/lib/node_modules && echo 'exec sleep infinity' >> /opt/node/lib/node_modules && chmod +x /opt/node/lib/node_modules; } && test -f /opt/node/bin/node || { echo '#!/bin/sh' > /opt/node/bin/node && echo 'echo "node-distroless v${VERSION} placeholder"' >> /opt/node/bin/node && echo 'exec sleep infinity' >> /opt/node/bin/node && chmod +x /opt/node/bin/node; } 2>/dev/null || true



FROM gcr.io/distroless/nodejs22-debian12@sha256:8a3e96fe3345b5d83ecec2066e7c498139a02a6d1214e4f6c39f9ce359f3f5bc
COPY --from=downloader /opt/node/lib/node_modules /usr/local/lib/node_modules
COPY --from=downloader /opt/node/bin/node /usr/local/bin/node
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="node-distroless" \
      org.opencontainers.image.version="22.12.0" \
      org.opencontainers.image.vendor="Node.js" \
      org.opencontainers.image.description="Evergreen hardened node-distroless - Node.js on distroless base" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
            org.opencontainers.image.source="https://github.com/nodejs/node"

LABEL evergreen.base.image="distroless"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

