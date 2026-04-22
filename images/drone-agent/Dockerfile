# =============================================================================
# SOVEREIGN HARDENED DRONE-AGENT
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=2.28.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/harness/drone/releases/download/v2.28.1/drone_linux_amd64.tar.gz" -o /tmp/archive.tar.gz &&     tar -xzf /tmp/archive.tar.gz -C /tmp &&     mv /tmp/drone-agent /tmp/drone-agent_stripped &&     strip /tmp/drone-agent_stripped &&     chmod +x /tmp/drone-agent_stripped

FROM scratch
COPY --from=downloader /tmp/drone-agent_stripped /usr/local/bin/drone-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/drone-agent", "--version"]
ENTRYPOINT ["/usr/local/bin/drone-agent"]
LABEL org.opencontainers.image.title="drone-agent"       org.opencontainers.image.description="Drone Agent - CI/CD build agent for Drone"       org.opencontainers.image.version="2.28.1"       org.opencontainers.image.vendor="Harness"       org.opencontainers.image.source="https://github.com/harness/drone"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
