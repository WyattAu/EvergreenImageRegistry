# =============================================================================
# SOVEREIGN HARDENED GOGS
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=0.13.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/gogs/gogs/releases/download/v0.13.0/gogs_0.13.0_linux_amd64.tar.gz" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gogs
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/gogs", "--version"]
ENTRYPOINT ["/usr/local/bin/gogs"]
LABEL org.opencontainers.image.title="gogs"       org.opencontainers.image.description="Gogs - lightweight self-hosted Git service"       org.opencontainers.image.version="0.13.0"       org.opencontainers.image.vendor="Gogs"       org.opencontainers.image.source="https://github.com/gogs/gogs"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
