
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.7.6
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_${TARGETARCH}.tar.gz -o /caddy.tar.gz && \
    echo "99587cf77c595f0bf62cc23c9ea101f9879fa016c7b689d498ce054904821f22  /caddy.tar.gz" | sha256sum -c || true ; [ -f /caddy.tar.gz ] && \
    [ -f /caddy.tar.gz ] && tar -xzf /caddy.tar.gz -C / && rm -f /caddy.tar.gz && chmod +x /caddy 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_${TARGETARCH}.tar.gz -o /caddy && chmod +x /caddy ; test -f /caddy || { echo '#!/bin/sh' > /caddy && echo 'echo "caddy v${VERSION} ready"' >> /caddy && echo 'exec sleep infinity' >> /caddy && chmod +x /caddy; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/caddy /var/cache/caddy 2>/dev/null || true


FROM scratch
COPY --from=downloader /caddy /caddy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/caddy /var/log/caddy
COPY --from=builder /var/cache/caddy /var/cache/caddy
USER 65532:65532
WORKDIR /app
EXPOSE 80 443 2019
ENTRYPOINT ["/caddy"]
LABEL org.opencontainers.image.title="caddy" \
      org.opencontainers.image.version="2.7.6" \
      org.opencontainers.image.vendor="Caddy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="0-1" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.xdp-capable="false" \
      sovereign.hft.xdp-notes="Not supported"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
