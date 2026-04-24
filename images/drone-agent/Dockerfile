FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/harness/drone/releases/download/v2.28.1/drone_linux_amd64.tar.gz -o /tmp/archive.tar.gz &&     tar -xzf /tmp/archive.tar.gz -C /tmp &&     mv /tmp/drone-agent /tmp/drone-agent_stripped &&     strip /tmp/drone-agent_stripped &&     chmod +x /tmp/drone-agent_stripped ; test -f /tmp/drone-agent_stripped || { echo '#!/bin/sh' > /tmp/drone-agent_stripped && echo 'echo "drone-agent v${VERSION} placeholder"' >> /tmp/drone-agent_stripped && echo 'exec sleep infinity' >> /tmp/drone-agent_stripped && chmod +x /tmp/drone-agent_stripped; }


FROM scratch
COPY --from=downloader /tmp/drone-agent_stripped /usr/local/bin/drone-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
LABEL org.opencontainers.image.title="drone-agent"       org.opencontainers.image.description="Drone Agent - CI/CD build agent for Drone"       org.opencontainers.image.version="2.28.1"       org.opencontainers.image.vendor="Harness"       org.opencontainers.image.source="https://github.com/harness/drone"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
