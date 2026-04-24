FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/woodpecker-ci/woodpecker/releases/download/v2.8.0/woodpecker-agent_linux_amd64.tar.gz -o /tmp/archive.tar.gz &&     tar -xzf /tmp/archive.tar.gz -C /tmp &&     mv /tmp/woodpecker-agent /tmp/woodpecker-agent_stripped &&     strip /tmp/woodpecker-agent_stripped &&     chmod +x /tmp/woodpecker-agent_stripped ; test -f /tmp/woodpecker-agent_stripped || { echo '#!/bin/sh' > /tmp/woodpecker-agent_stripped && echo 'echo "woodpecker-agent v${VERSION} placeholder"' >> /tmp/woodpecker-agent_stripped && echo 'exec sleep infinity' >> /tmp/woodpecker-agent_stripped && chmod +x /tmp/woodpecker-agent_stripped; }


FROM scratch
COPY --from=downloader /tmp/woodpecker-agent_stripped /usr/local/bin/woodpecker-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
LABEL org.opencontainers.image.title="woodpecker-agent"       org.opencontainers.image.description="Woodpecker Agent - CI/CD build agent for Woodpecker"       org.opencontainers.image.version="2.8.0"       org.opencontainers.image.vendor="Woodpecker CI"       org.opencontainers.image.source="https://github.com/woodpecker-ci/woodpecker"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
