ARG VERSION=v4.1.3
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532



ARG SHIM_VERSION=v0.2.0

FROM localai/localai:v4.1.3@sha256:e10d6545b51bae2ab03fdb37183fd921850afd51b06285ede9b0e326fa562156 AS upstream



FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=v4.1.3

RUN apk add --no-cache ca-certificates


COPY --from=upstream /build/localai-loadbalancer /usr/local/bin/localai-loadbalancer

RUN chmod +x /usr/local/bin/localai-loadbalancer && mkdir -p /app /var/log/localai-loadbalancer /var/cache/localai-loadbalancer && chown -R 65532:65532 /app /var/log/localai-loadbalancer /var/cache/localai-loadbalancer

USER 65532:65532

WORKDIR /app

EXPOSE 8080




HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]

LABEL org.opencontainers.image.title="localai-loadbalancer"       org.opencontainers.image.version="v4.1.3"       org.opencontainers.image.vendor="mudler/LocalAI"       org.opencontainers.image.source="https://github.com/mudler/LocalAI"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.base="wolfi"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
org.opencontainers.image.description="localai-loadbalancer container image" \
evergreen.base.image="wolfi"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
