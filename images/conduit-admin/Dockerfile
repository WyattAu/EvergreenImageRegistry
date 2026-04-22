# =============================================================================
# SOVEREIGN HARDENED CONDUIT-ADMIN
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=0.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/famedly/conduit/releases/download/v0.8.0/conduit-x86_64-unknown-linux-musl" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/conduit
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 6167
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/conduit", "--version"]
ENTRYPOINT ["/usr/local/bin/conduit"]
LABEL org.opencontainers.image.title="conduit-admin"       org.opencontainers.image.description="Conduit Admin - Conduit Matrix homeserver with admin interface"       org.opencontainers.image.version="0.8.0"       org.opencontainers.image.vendor="Famedly"       org.opencontainers.image.source="https://github.com/famedly/conduit"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
