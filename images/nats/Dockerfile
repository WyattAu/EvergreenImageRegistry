ARG VERSION=v2.14.3
ARG SHIM_VERSION=v2.0.0

FROM ghcr.io/wyattau/evergreenimageregistry/mirror-debian-bookworm-slim:latest AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    arch=$(case ${TARGETARCH} in amd64) echo "amd64";; arm64) echo "arm64";; *) echo "amd64";; esac) && \
    curl -fsSL "https://github.com/nats-io/nats-server/releases/download/${VERSION}/nats-server-${VERSION}-linux-${arch}.tar.gz" -o /tmp/nats.tar.gz && \
    tar -xzf /tmp/nats.tar.gz -C /tmp && \
    cp /tmp/nats-server-${VERSION}-linux-${arch}/nats-server /nats-server && \
    chmod +x /nats-server

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /nats-server /usr/local/bin/nats-server

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

EXPOSE 4222 9101
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:4222"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/nats-server"]
CMD []

LABEL org.opencontainers.image.title="nats" evergreen.image.tier="critical" evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="scratch" evergreen.security.cap-drop="ALL"
STOPSIGNAL SIGTERM
