# =============================================================================
# SOVEREIGN HARDENED WOODPECKER-AGENT
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=2.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/woodpecker-ci/woodpecker/releases/download/v2.8.0/woodpecker-agent_linux_amd64.tar.gz" -o /tmp/archive.tar.gz &&     tar -xzf /tmp/archive.tar.gz -C /tmp &&     mv /tmp/woodpecker-agent /tmp/woodpecker-agent_stripped &&     strip /tmp/woodpecker-agent_stripped &&     chmod +x /tmp/woodpecker-agent_stripped

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