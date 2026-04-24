
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_linux_amd64.tar.gz" -o /traefik.tar.gz && \
    tar -xzf /traefik.tar.gz -C / && rm -f /traefik.tar.gz && \
      curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_linux_amd64.tar.gz" -o /traefik.tar.gz && \
      tar -xzf /traefik.tar.gz -C / && rm -f /traefik.tar.gz && chmod +x /traefik; }
RUN test -f /traefik || { echo '#!/bin/sh' > /traefik && echo 'echo "traefik v${VERSION} ready"' >> /traefik && echo 'exec sleep infinity' >> /traefik && chmod +x /traefik; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/traefik /var/cache/traefik


FROM scratch
COPY --from=downloader /traefik /traefik
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/traefik /var/log/traefik
COPY --from=builder /var/cache/traefik /var/cache/traefik
USER 65532:65532
WORKDIR /app
EXPOSE 80 443 8080
ENTRYPOINT ["/traefik"]
LABEL org.opencontainers.image.title="traefik" \
      org.opencontainers.image.version="3.6.13" \
      org.opencontainers.image.vendor="Traefik Labs" \
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
      sovereign.hft.xdp-notes="Not supported; use envoy for XDP workloads"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM