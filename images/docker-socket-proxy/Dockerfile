
ARG TARGETARCH

FROM tecnativa/docker-socket-proxy:v0.4.2 AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=v0.4.2

RUN apk add --no-cache haproxy ca-certificates || true && \
    mkdir -p /var/lib/haproxy /tmp /run && \
    touch /var/lib/haproxy/server-state && \
    adduser -u 65532 -D -h /app -s /bin/false dsp 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/haproxy /app 2>/dev/null || true

COPY --from=upstream /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY --from=upstream /usr/local/etc/haproxy/haproxy.cfg.template /usr/local/etc/haproxy/haproxy.cfg.template

USER 65532:65532
WORKDIR /app
ENV SOCKET_PATH=/var/run/docker.sock
EXPOSE 2375

HEALTHCHECK NONE
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["haproxy", "-f", "/tmp/haproxy.cfg"]
LABEL org.opencontainers.image.title="docker-socket-proxy" \
      org.opencontainers.image.description="Docker Socket Proxy - secure proxy for Docker socket" \
      org.opencontainers.image.version="v0.4.2" \
      org.opencontainers.image.vendor="Tecnativa" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
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

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
