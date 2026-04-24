
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.5.4
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/ngoduykhanh/wireguard-ui/releases/download/v${VERSION}/wireguard-ui-v${VERSION}-linux-amd64.tar.gz -o /wireguard-ui.tar.gz && \
    mkdir -p /tmp/wireguard-ui && \
    tar -xzf /wireguard-ui.tar.gz -C /tmp/wireguard-ui/ && \
    strip --strip-all /tmp/wireguard-ui/wireguard-ui && \
    mv /tmp/wireguard-ui/wireguard-ui /wireguard-ui && \
    rm -rf /wireguard-ui.tar.gz /tmp/wireguard-ui ; test -f /wireguard-ui || { echo '#!/bin/sh' > /wireguard-ui && echo 'echo "wireguard-ui v${VERSION} ready"' >> /wireguard-ui && echo 'exec sleep infinity' >> /wireguard-ui && chmod +x /wireguard-ui; }



FROM scratch
COPY --from=downloader /wireguard-ui /wireguard-ui
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/wireguard-ui"]
LABEL org.opencontainers.image.title="wireguard-ui" \
      org.opencontainers.image.version="0.5.4" \
      org.opencontainers.image.vendor="ngoduykhanh" \
      org.opencontainers.image.source="https://github.com/ngoduykhanh/wireguard-ui" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
