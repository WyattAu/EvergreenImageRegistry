
ARG TARGETARCH

FROM tecnativa/docker-socket-proxy:v0.4.2 AS upstream
ARG TARGETARCH

FROM scratch
ARG VERSION=v0.4.2
COPY --from=upstream /docker-socket-proxy /docker-socket-proxy
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 2375

HEALTHCHECK NONE
ENTRYPOINT ["/docker-socket-proxy"]
LABEL org.opencontainers.image.title="docker-socket-proxy" \
      org.opencontainers.image.description="Docker Socket Proxy - secure proxy for Docker socket" \
      org.opencontainers.image.version="v0.4.2" \
      org.opencontainers.image.vendor="Tecnativa" \
      evergreen.image.tier="critical" \
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
