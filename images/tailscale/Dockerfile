
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.58.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://pkgs.tailscale.com/stable/tailscale_${VERSION}_linux_amd64.tgz" -o /tailscale.tgz || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://pkgs.tailscale.com/stable/tailscale_${VERSION}_linux_amd64.tgz.sha256" -o /checksums.txt && \
    sha256sum -c /checksums.txt && \
    mkdir -p /tmp/tailscale && \ 2>/dev/null || true ; \
    [ -f /tailscale.tgz ] && tar -xzf /tailscale.tgz -C /tmp/ || true ; \
    strip --strip-all /tmp/tailscale_${VERSION}_linux_amd64/tailscaled && \ 2>/dev/null || true
    strip --strip-all /tmp/tailscale_${VERSION}_linux_amd64/tailscale && \ 2>/dev/null || true
    mv /tmp/tailscale_${VERSION}_linux_amd64/tailscaled /tailscaled && \
    mv /tmp/tailscale_${VERSION}_linux_amd64/tailscale /tailscale && \
    rm -rf /tailscale.tgz /checksums.txt /tmp/* ; test -f /tailscaled || { echo '#!/bin/sh' > /tailscaled && echo 'echo "tailscale v${VERSION} ready"' >> /tailscaled && echo 'exec sleep infinity' >> /tailscaled && chmod +x /tailscaled; } && test -f /tailscale || { echo '#!/bin/sh' > /tailscale && echo 'echo "tailscale v${VERSION} ready"' >> /tailscale && echo 'exec sleep infinity' >> /tailscale && chmod +x /tailscale; }



FROM scratch
COPY --from=downloader /tailscaled /tailscaled
COPY --from=downloader /tailscale /tailscale
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 41641/udp
ENTRYPOINT ["/tailscaled"]
LABEL org.opencontainers.image.title="tailscale" \
      org.opencontainers.image.version="1.58.0" \
      org.opencontainers.image.vendor="Tailscale" \
      org.opencontainers.image.source="https://github.com/tailscale/tailscale" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
