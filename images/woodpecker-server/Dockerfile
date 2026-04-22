# =============================================================================
# SOVEREIGN HARDENED WOODPECKER-SERVER
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=2.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/woodpecker-ci/woodpecker/releases/download/v2.8.0/woodpecker-server_linux_amd64.tar.gz" -o /tmp/archive.tar.gz &&     tar -xzf /tmp/archive.tar.gz -C /tmp &&     mv /tmp/woodpecker-server /tmp/woodpecker-server_stripped &&     strip /tmp/woodpecker-server_stripped &&     chmod +x /tmp/woodpecker-server_stripped

FROM scratch
COPY --from=downloader /tmp/woodpecker-server_stripped /usr/local/bin/woodpecker-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/woodpecker-server", "--version"]
ENTRYPOINT ["/usr/local/bin/woodpecker-server"]
LABEL org.opencontainers.image.title="woodpecker-server"       org.opencontainers.image.description="Woodpecker Server - CI/CD server for Woodpecker CI"       org.opencontainers.image.version="2.8.0"       org.opencontainers.image.vendor="Woodpecker CI"       org.opencontainers.image.source="https://github.com/woodpecker-ci/woodpecker"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
