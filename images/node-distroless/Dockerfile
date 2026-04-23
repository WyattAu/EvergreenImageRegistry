ARG VERSION=v22.12.0
ARG BUILD_DATE

FROM gcr.io/distroless/nodejs22-debian12:latest AS base

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz" -o /node.tar.xz && \
    mkdir -p /opt/node && tar -xf /node.tar.xz -C /opt/node --strip-components=1 && rm /node.tar.xz

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