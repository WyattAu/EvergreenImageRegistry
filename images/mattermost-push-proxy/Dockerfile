# =============================================================================
# SOVEREIGN HARDENED MATTERMOST-PUSH-PROXY
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=11.6.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://releases.mattermost.com/mattermost/11.6.0/mattermost-11.6.0-linux-amd64.tar.gz" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/mattermost-push-proxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 8065
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/mattermost-push-proxy", "--version"]
ENTRYPOINT ["/usr/local/bin/mattermost-push-proxy"]
LABEL org.opencontainers.image.title="mattermost-push-proxy"       org.opencontainers.image.description="Mattermost Push Proxy - push notification proxy for Mattermost"       org.opencontainers.image.version="11.6.0"       org.opencontainers.image.vendor="Mattermost"       org.opencontainers.image.source="https://github.com/mattermost/mattermost"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
