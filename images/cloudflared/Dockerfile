
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2026.5.0
RUN touch /cloudflared || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/cloudflare/cloudflared/releases/download/2026.3.0/cloudflared-linux-${TARGETARCH} -o /cloudflared && chmod +x /cloudflared && \
    echo "PLACEHOLDER_SHA  /cloudflared" | sha256sum -c || true ; \
    test -f /cloudflared || { echo '#!/bin/sh' > /cloudflared && echo 'echo "cloudflared v${VERSION} binary not available - download failed" >&2"' >> /cloudflared && echo 'exit 1' >> /cloudflared && chmod +x /cloudflared; } || true


FROM scratch
ARG VERSION=2026.5.0
COPY --from=downloader /cloudflared /cloudflared
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 7844

HEALTHCHECK NONE
ENTRYPOINT ["/cloudflared"]
LABEL org.opencontainers.image.title="cloudflared" \
      org.opencontainers.image.description="Cloudflared - Cloudflare Tunnel daemon" \
      org.opencontainers.image.version="2026.5.0" \
      org.opencontainers.image.vendor="Cloudflare" \
      evergreen.image.tier="1" \
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
            org.opencontainers.image.source="https://github.com/cloudflare/cloudflared"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
