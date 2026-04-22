# =============================================================================
# SOVEREIGN HARDENED GOTIFY
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=2.4.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/gotify/server/releases/download/v2.4.0/gotify-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gotify
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/gotify", "--version"]
ENTRYPOINT ["/usr/local/bin/gotify"]
LABEL org.opencontainers.image.title="gotify"       org.opencontainers.image.description="Gotify - simple push notification server"       org.opencontainers.image.version="2.4.0"       org.opencontainers.image.vendor="Gotify"       org.opencontainers.image.source="https://github.com/gotify/server"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
