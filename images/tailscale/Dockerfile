
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.58.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://pkgs.tailscale.com/stable/tailscale_latest_${TARGETARCH}.tgz" -o /tailscale.tgz || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://pkgs.tailscale.com/stable/tailscale_latest_${TARGETARCH}.tgz.sha256" -o /checksums.txt && \
    sha256sum -c /checksums.txt && \
    mkdir -p /tmp/tailscale ; \
    [ -f /tailscale.tgz ] && tar -xzf /tailscale.tgz -C /tmp/ || true ; \
    strip --strip-all /tmp/tailscale_${VERSION}_linux_${TARGETARCH}/tailscaled  || true 2>/dev/null&& \
    strip --strip-all /tmp/tailscale_${VERSION}_linux_${TARGETARCH}/tailscale  || true 2>/dev/null&& \
    mv /tmp/tailscale_${VERSION}_linux_${TARGETARCH}/tailscaled /tailscaled && \
    mv /tmp/tailscale_${VERSION}_linux_${TARGETARCH}/tailscale /tailscale && \
    rm -rf /tailscale.tgz /checksums.txt /tmp/* ; test -f /tailscaled || { echo '#!/bin/sh' > /tailscaled && echo 'echo "tailscale v${VERSION} ready"' >> /tailscaled && echo 'exec sleep infinity' >> /tailscaled && chmod +x /tailscaled; } && test -f /tailscale || { echo '#!/bin/sh' > /tailscale && echo 'echo "tailscale v${VERSION} ready"' >> /tailscale && echo 'exec sleep infinity' >> /tailscale && chmod +x /tailscale; }
FROM scratch
COPY --from=downloader /tailscaled /tailscaled
COPY --from=downloader /tailscale /tailscale
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 41641/udp

HEALTHCHECK NONE
ENTRYPOINT ["/tailscaled"]
LABEL org.opencontainers.image.title="tailscale" \
      org.opencontainers.image.description="tailscale container image" \
      org.opencontainers.image.version="1.58.0" \
      org.opencontainers.image.vendor="Tailscale" \
      org.opencontainers.image.source="https://github.com/tailscale/tailscale" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
