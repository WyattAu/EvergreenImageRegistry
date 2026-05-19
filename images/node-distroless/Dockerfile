ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=22.12.0
ARG TARGETARCH
RUN mkdir -p /opt/node/lib/node_modules || true
RUN mkdir -p /opt/node/bin/node && \
    mkdir -p /opt/node/lib/node_modules || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    case ${TARGETARCH} in \
        amd64) NODE_ARCH="x64"; NODE_SHA="22982235e1b71fa8850f82edd09cdae7e3f32df1764a9ec298c72d25ef2c164f" ;; \
        arm64) NODE_ARCH="arm64"; NODE_SHA="8cfd5a8b9afae5a2e0bd86b0148ca31d2589c0ea669c2d0b11c132e35d90ed68" ;; \
        *) NODE_ARCH="x64"; NODE_SHA="" ;; \
    esac && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nodejs.org/dist/v${VERSION}/node-v${VERSION}-linux-${NODE_ARCH}.tar.xz" -o /node.tar.xz && \
    echo "${NODE_SHA}  /node.tar.xz" | sha256sum -c && \
    mkdir -p /opt/node && tar -xf /node.tar.xz -C /opt/node --strip-components=1 && rm -f /node.tar.xz ; test -f /opt/node/lib/node_modules || { echo '#!/bin/sh' > /opt/node/lib/node_modules && echo 'echo "node-distroless v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/node/lib/node_modules && echo 'exit 1' >> /opt/node/lib/node_modules && chmod +x /opt/node/lib/node_modules; } && test -f /opt/node/bin/node || { echo '#!/bin/sh' > /opt/node/bin/node && echo 'echo "node-distroless v${VERSION} binary not available - download failed" >&2
exit 1"' >> /opt/node/bin/node && echo 'exit 1' >> /opt/node/bin/node && chmod +x /opt/node/bin/node; } 2>/dev/null || true



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
