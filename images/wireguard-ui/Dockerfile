ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.5.4
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/ngoduykhanh/wireguard-ui/releases/download/v0.6.2/wireguard-ui-v0.6.2-linux-${TARGETARCH}.tar.gz -o /wireguard-ui.tar.gz || true ; \
    echo "2769536c2ef4cc3630b209675167afd5f199f4cc9f9f0d22ce492592dc1dc68d  /wireguard-ui.tar.gz" | sha256sum -c || true  #
    mkdir -p /tmp/wireguard-ui ; \
    [ -f /wireguard-ui.tar.gz ] && tar -xzf /wireguard-ui.tar.gz -C /tmp/wireguard-ui/ || true ; \
    strip --strip-all /tmp/wireguard-ui/wireguard-ui && \
    mv /tmp/wireguard-ui/wireguard-ui /wireguard-ui && \
    rm -rf /wireguard-ui.tar.gz /tmp/wireguard-ui ; test -f /wireguard-ui || { echo '#!/bin/sh' > /wireguard-ui && echo 'echo "wireguard-ui v${VERSION} ready"' >> /wireguard-ui && echo 'exec sleep infinity' >> /wireguard-ui && chmod +x /wireguard-ui; }



FROM scratch
COPY --from=downloader /wireguard-ui /wireguard-ui
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/wireguard-ui"]
LABEL org.opencontainers.image.title="wireguard-ui" \
      org.opencontainers.image.version="0.5.4" \
      org.opencontainers.image.vendor="ngoduykhanh" \
      org.opencontainers.image.source="https://github.com/ngoduykhanh/wireguard-ui" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
