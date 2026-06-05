
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM tecnativa/docker-socket-proxy:v0.4.2@sha256:5571c19d8e5c1a58a4edb5781beedb3065d6995985e5ca2f1003c016e266517c AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=v0.4.2

RUN apk add --no-cache haproxy ca-certificates && \
    mkdir -p /var/lib/haproxy /tmp /run && \
    touch /var/lib/haproxy/server-state && \
    adduser -u 65532 -D -h /app -s /bin/false dsp 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/haproxy /app /run /usr/local/etc/haproxy 2>/dev/null || true

COPY --from=upstream /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY --from=upstream /usr/local/etc/haproxy/haproxy.cfg.template /usr/local/etc/haproxy/haproxy.cfg.template
COPY --from=upstream /usr/local/etc/haproxy/errors /usr/local/etc/haproxy/errors

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
ENV SOCKET_PATH=/var/run/docker.sock
EXPOSE 2375

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:2375"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "docker-entrypoint.sh", "--", "haproxy", "-f", "/tmp/haproxy.cfg"]
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
