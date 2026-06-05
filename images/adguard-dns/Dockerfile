
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.107.50
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/AdguardTeam/AdGuardHome/releases/download/v${VERSION}/AdGuardHome_linux_${TARGETARCH}.tar.gz -o /AdGuardHome.tar.gz ; \
    echo "baf34fbd8cbaf4ff049d4b5239527c8b6921f2102ac0452803c5f68700cb123a  /AdGuardHome.tar.gz" | sha256sum -c ; \
    [ -f /AdGuardHome.tar.gz ] && tar -xzf /AdGuardHome.tar.gz -C / && rm -f /AdGuardHome.tar.gz ; \
    chmod +x /AdGuardHome && \
    strip --strip-all /AdGuardHome 2>/dev/null 2>/dev/nullbinary not available - download failed" >&2"' >> /AdGuardHome && echo 'exit 1' >> /AdGuardHome && chmod +x /AdGuardHome; } 2>/dev/null



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/AdGuardHome /var/cache/AdGuardHome /opt/AdGuardHome/data 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /AdGuardHome /AdGuardHome
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/AdGuardHome /var/log/AdGuardHome
COPY --from=builder /var/cache/AdGuardHome /var/cache/AdGuardHome
COPY --from=builder /opt/AdGuardHome/data /opt/AdGuardHome/data
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 3000 443 853

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:53"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="adguard-dns" \
      org.opencontainers.image.version="0.107.50" \
      org.opencontainers.image.vendor="AdGuard" \
      org.opencontainers.image.source="https://github.com/AdguardTeam/AdGuardHome" \
      org.opencontainers.image.description="AdGuard Home DNS server" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
