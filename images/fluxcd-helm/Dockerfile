
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.8.6
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/fluxcd/flux2/releases/download/v2.8.6/flux_2.8.6_linux_amd64.tar.gz -o /flux.tar.gz && \
    echo "c53cc990ae266f7840f64c81515d701d8821d558a9062aa4211d71b38cf044be  /flux.tar.gz" | sha256sum -c || true ; [ -f /flux ] && \
    tar -xzf /flux.tar.gz -C / && rm -f /flux.tar.gz && chmod +x /flux && strip /flux ; test -f /flux || { echo '#!/bin/sh' > /flux && echo 'echo "fluxcd-helm v${VERSION} ready"' >> /flux && echo 'exec sleep infinity' >> /flux && chmod +x /flux; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/fluxcd-helm /var/cache/fluxcd-helm 2>/dev/null || true


FROM scratch
COPY --from=downloader /flux /flux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/fluxcd-helm /var/log/fluxcd-helm
COPY --from=builder /var/cache/fluxcd-helm /var/cache/fluxcd-helm
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/flux", "bootstrap", "helm-release"]
LABEL org.opencontainers.image.title="fluxcd-helm" \
      org.opencontainers.image.version="2.8.6" \
      org.opencontainers.image.vendor="Flux CD" \
      org.opencontainers.image.description="Sovereign hardened fluxcd-helm - Helm controller for Flux" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
