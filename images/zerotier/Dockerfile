ARG VERSION=1.12.2
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM zerotier/zerotier:${VERSION} AS upstream

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache libstdc++ ca-certificates iproute2
COPY --from=upstream /usr/sbin/zerotier-one /usr/sbin/zerotier-one

WORKDIR /app

EXPOSE 9993/udp 9993/tcp
EXPOSE 9101

LABEL org.opencontainers.image.title="zerotier" org.opencontainers.image.version="1.12.2" org.opencontainers.image.vendor="ZeroTier" org.opencontainers.image.source="https://github.com/zerotier/ZeroTierOne" evergreen.image.tier="1" evergreen.image.category="networking" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.distrole="debian-slim" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.description="zerotier container image" \
evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9993"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]

CMD ["-c", "/usr/sbin/zerotier-one", "--", "-p9993"]
