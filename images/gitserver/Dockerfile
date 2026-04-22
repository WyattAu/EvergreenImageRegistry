# =============================================================================
# SOVEREIGN HARDENED GITSERVER
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=0.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/go-gitea/gitea/releases/download/v1.21.10/gitea-1.21.10-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gitserver
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/gitserver", "--version"]
ENTRYPOINT ["/usr/local/bin/gitserver"]
LABEL org.opencontainers.image.title="gitserver"       org.opencontainers.image.description="GitServer - lightweight git HTTP server for bare repositories"       org.opencontainers.image.version="0.1.0"       org.opencontainers.image.vendor="Generic"       org.opencontainers.image.source="https://github.com/go-gitea/gitea"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
