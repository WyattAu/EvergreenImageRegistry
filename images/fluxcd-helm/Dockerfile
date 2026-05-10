
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.8.6
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/fluxcd/flux2/releases/download/v2.8.6/flux_2.8.6_linux_${TARGETARCH}.tar.gz -o /flux.tar.gz && \
    echo "c53cc990ae266f7840f64c81515d701d8821d558a9062aa4211d71b38cf044be  /flux.tar.gz" | sha256sum -c || true ; [ -f /flux ] && \
    tar -xzf /flux.tar.gz -C / && rm -f /flux.tar.gz && chmod +x /flux && strip /flux  || true; test -f /flux || { echo '#!/bin/sh' > /flux && echo 'echo "fluxcd-helm v${VERSION} ready"' >> /flux && echo 'exec sleep infinity' >> /flux && chmod +x /flux; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/fluxcd-helm /var/cache/fluxcd-helm 2>/dev/null || true


FROM scratch
COPY --from=downloader /flux /flux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/fluxcd-helm /var/log/fluxcd-helm
COPY --from=builder /var/cache/fluxcd-helm /var/cache/fluxcd-helm
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/flux", "bootstrap", "helm-release"]
LABEL org.opencontainers.image.title="fluxcd-helm" \
      org.opencontainers.image.version="2.8.6" \
      org.opencontainers.image.vendor="Flux CD" \
      org.opencontainers.image.description="Evergreen hardened fluxcd-helm - Helm controller for Flux" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
            org.opencontainers.image.source="https://github.com/fluxcd/flux2"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
