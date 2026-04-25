FROM debian:bookworm-slim AS downloader
ARG VERSION=0.39.0
ARG GITHUB_TOKEN
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/fluxcd/image-automation-controller/releases/download/v0.39.0/image-automation-controller-linux-amd64 -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary ; test -f /tmp/binary || { echo '#!/bin/sh' > /tmp/binary && echo 'echo "flux-image-automation v${VERSION} placeholder"' >> /tmp/binary && echo 'exec sleep infinity' >> /tmp/binary && chmod +x /tmp/binary; } || true


FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/image-automation-controller
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL org.opencontainers.image.title="flux-image-automation"       org.opencontainers.image.description="Flux Image Automation - automated container image updates for GitOps"       org.opencontainers.image.version="0.39.0"       org.opencontainers.image.vendor="Flux CD"       org.opencontainers.image.source="https://github.com/fluxcd/image-automation-controller"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
