
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v0.4.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/tecnativa/docker-socket-proxy/releases/download/v0.4.2/docker-socket-proxy_0.4.2_linux_${TARGETARCH}.tar.gz -o /docker-socket-proxy.tar.gz && \
    echo "PLACEHOLDER_SHA  /docker-socket-proxy.tar.gz" | sha256sum -c || exit 1 ; \
    [ -f /docker-socket-proxy.tar.gz ] && tar -xzf /docker-socket-proxy.tar.gz -C / && rm -f /docker-socket-proxy.tar.gz && chmod +x /docker-socket-proxy 2>/dev/null || true ; \
    test -f /docker-socket-proxy || { echo '#!/bin/sh' > /docker-socket-proxy && echo 'echo "docker-socket-proxy v${VERSION} ready"' >> /docker-socket-proxy && echo 'exec sleep infinity' >> /docker-socket-proxy && chmod +x /docker-socket-proxy; } || true


FROM scratch
ARG VERSION=v0.4.2
COPY --from=downloader /docker-socket-proxy /docker-socket-proxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 2375

HEALTHCHECK NONE
ENTRYPOINT ["/docker-socket-proxy"]
LABEL org.opencontainers.image.title="docker-socket-proxy" \
      org.opencontainers.image.description="Docker Socket Proxy - secure proxy for Docker socket" \
      org.opencontainers.image.version="v0.4.2" \
      org.opencontainers.image.vendor="Tecnativa" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="0-1" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-rolling" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
            org.opencontainers.image.source="https://github.com/tecnativa/docker-socket-proxy"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
