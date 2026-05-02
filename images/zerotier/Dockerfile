ARG VERSION=latest

FROM zerotier/zerotier:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libstdc++ ca-certificates iproute2 || true
COPY --from=upstream /usr/sbin/zerotier-one /usr/sbin/zerotier-one

WORKDIR /app

EXPOSE 9993/udp 9993/tcp
EXPOSE 9101

LABEL org.opencontainers.image.title="zerotier" org.opencontainers.image.version="1.12.2" org.opencontainers.image.vendor="ZeroTier" org.opencontainers.image.source="https://github.com/zerotier/ZeroTierOne" sovereign.image.tier="1" sovereign.image.category="networking" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.distrole="debian-slim" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="3s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/usr/sbin/zerotier-one"]

CMD ["-p9993"]
