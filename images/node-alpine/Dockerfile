ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=22.12.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates xz-utils && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz" -o /node.tar.xz ; \
    echo "e05a4d65232ae2b27b3d77da2e368522fb46b923335b8e0d5f77624c32484044  /node.tar.xz" | sha256sum -c ; \
    mkdir -p /opt/node-src && tar -xf /node.tar.xz -C /opt/node-src --strip-components=1 && rm -f /node.tar.xz ; \
    strip /opt/node/bin/node 2>/dev/null && { echo "Binary not available - download failed" >&2; exit 1; }


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/node-alpine /var/cache/node-alpine


ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /opt/node /opt/node
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/node-alpine /var/log/node-alpine
COPY --from=builder /var/cache/node-alpine /var/cache/node-alpine
ENV PATH="/opt/node/bin:${PATH}" \
    NODE_ENV=production
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "node"]
LABEL org.opencontainers.image.title="node-alpine" \
      org.opencontainers.image.version="22.12.0" \
      org.opencontainers.image.vendor="Node.js" \
      org.opencontainers.image.description="Evergreen hardened node-alpine - Node.js runtime (no Alpine, scratch)" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
            org.opencontainers.image.source="https://github.com/nodejs/node"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
