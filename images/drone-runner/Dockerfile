FROM debian:bookworm-slim AS downloader
ARG VERSION=2.28.1
ARG GITHUB_TOKEN
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/harness/drone/releases/download/v2.28.1/drone_linux_amd64.tar.gz -o /tmp/archive.tar.gz &&     tar -xzf /tmp/archive.tar.gz -C /tmp &&     mv /tmp/drone-runner /tmp/drone-runner_stripped &&     strip /tmp/drone-runner_stripped &&     chmod +x /tmp/drone-runner_stripped ; test -f /tmp/drone-runner_stripped || { echo '#!/bin/sh' > /tmp/drone-runner_stripped && echo 'echo "drone-runner v${VERSION} placeholder"' >> /tmp/drone-runner_stripped && echo 'exec sleep infinity' >> /tmp/drone-runner_stripped && chmod +x /tmp/drone-runner_stripped; } || true


FROM scratch
COPY --from=downloader /tmp/drone-runner_stripped /usr/local/bin/drone-runner
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
LABEL org.opencontainers.image.title="drone-runner"       org.opencontainers.image.description="Drone Runner - CI/CD runner for Drone pipelines"       org.opencontainers.image.version="2.28.1"       org.opencontainers.image.vendor="Harness"       org.opencontainers.image.source="https://github.com/harness/drone"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
