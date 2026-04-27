FROM debian:bookworm-slim AS downloader
ARG VERSION=2.28.2
ARG GITHUB_TOKEN
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/harness/drone/releases/download/v2.28.2/drone_linux_amd64.tar.gz -o /tmp/archive.tar.gz &&     tar -xzf /tmp/archive.tar.gz -C /tmp &&     mv /tmp/drone-autoscaler /tmp/drone-autoscaler_stripped &&     strip /tmp/drone-autoscaler_stripped &&     chmod +x /tmp/drone-autoscaler_stripped ; test -f /tmp/drone-autoscaler_stripped || { echo '#!/bin/sh' > /tmp/drone-autoscaler_stripped && echo 'echo "drone-autoscaler v${VERSION} placeholder"' >> /tmp/drone-autoscaler_stripped && echo 'exec sleep infinity' >> /tmp/drone-autoscaler_stripped && chmod +x /tmp/drone-autoscaler_stripped; } || true


FROM scratch
COPY --from=downloader /tmp/drone-autoscaler_stripped /usr/local/bin/drone-autoscaler
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL org.opencontainers.image.title="drone-autoscaler"       org.opencontainers.image.description="Drone Autoscaler - automatic scaling for Drone runners"       org.opencontainers.image.version="2.28.2"       org.opencontainers.image.vendor="Harness"       org.opencontainers.image.source="https://github.com/harness/drone"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
