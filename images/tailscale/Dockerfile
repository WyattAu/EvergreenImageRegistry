# =============================================================================
# SOVEREIGN HARDENED TAILSCALE
# Tailscale mesh VPN node (tailscaled + tailscale CLI)
# Constraint: scratch - Go static binaries, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.58.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://pkgs.tailscale.com/stable/tailscale_${VERSION}_linux_amd64.tgz" -o /tailscale.tgz && \
    curl -fsSL "https://pkgs.tailscale.com/stable/tailscale_${VERSION}_linux_amd64.tgz.sha256" -o /checksums.txt && \
    sha256sum -c /checksums.txt && \
    mkdir -p /tmp/tailscale && \
    tar -xzf /tailscale.tgz -C /tmp/ && \
    strip --strip-all /tmp/tailscale_${VERSION}_linux_amd64/tailscaled && \
    strip --strip-all /tmp/tailscale_${VERSION}_linux_amd64/tailscale && \
    mv /tmp/tailscale_${VERSION}_linux_amd64/tailscaled /tailscaled && \
    mv /tmp/tailscale_${VERSION}_linux_amd64/tailscale /tailscale && \
    rm -rf /tailscale.tgz /checksums.txt /tmp/*

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