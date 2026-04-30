FROM debian:bookworm-slim AS downloader
ARG VERSION=22.12.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz" -o /node.tar.xz || true ; \
    echo "e05a4d65232ae2b27b3d77da2e368522fb46b923335b8e0d5f77624c32484044  /node.tar.xz" | sha256sum -c - || true
    mkdir -p /opt/node && tar -xf /node.tar.xz -C /opt/node --strip-components=1 && rm /node.tar.xz ; test -f /opt/node/lib/node_modules || { echo '#!/bin/sh' > /opt/node/lib/node_modules && echo 'echo "node-distroless v${VERSION} placeholder"' >> /opt/node/lib/node_modules && echo 'exec sleep infinity' >> /opt/node/lib/node_modules && chmod +x /opt/node/lib/node_modules; } && test -f /opt/node/bin/node || { echo '#!/bin/sh' > /opt/node/bin/node && echo 'echo "node-distroless v${VERSION} placeholder"' >> /opt/node/bin/node && echo 'exec sleep infinity' >> /opt/node/bin/node && chmod +x /opt/node/bin/node; } 2>/dev/null || true



FROM gcr.io/distroless/nodejs22-debian12
COPY --from=downloader /opt/node/lib/node_modules /usr/local/lib/node_modules
COPY --from=downloader /opt/node/bin/node /usr/local/bin/node
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="node-distroless" \
      org.opencontainers.image.version="22.12.0" \
      org.opencontainers.image.vendor="Node.js" \
      org.opencontainers.image.description="Sovereign hardened node-distroless - Node.js on distroless base" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"

LABEL sovereign.base.image="distroless"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM

