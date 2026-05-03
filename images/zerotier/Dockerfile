ARG VERSION=latest

FROM zerotier/zerotier:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache libstdc++ ca-certificates iproute2 || true
COPY --from=upstream /usr/sbin/zerotier-one /usr/sbin/zerotier-one

WORKDIR /app

EXPOSE 9993/udp 9993/tcp
EXPOSE 9101

LABEL org.opencontainers.image.title="zerotier" org.opencontainers.image.version="1.12.2" org.opencontainers.image.vendor="ZeroTier" org.opencontainers.image.source="https://github.com/zerotier/ZeroTierOne" evergreen.image.tier="1" evergreen.image.category="networking" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.distrole="debian-slim" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9993/ || exit 1
ENTRYPOINT ["/usr/sbin/zerotier-one"]

CMD ["-p9993"]
