ARG VERSION=1.16.0
ARG TARGETARCH

FROM zerotier/zerotier:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache libstdc++ ca-certificates iproute2 || true
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

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9993/ || exit 1
ENTRYPOINT ["/usr/sbin/zerotier-one"]

CMD ["-p9993"]
