# =============================================================================
# SOVEREIGN HARDENED MATTERMOST-OPERATOR
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=1.10.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mattermost/mattermost-operator/releases/download/v1.10.0/mattermost-operator" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/mattermost-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL org.opencontainers.image.title="mattermost-operator"       org.opencontainers.image.description="Mattermost Operator - Kubernetes operator for Mattermost"       org.opencontainers.image.version="1.10.0"       org.opencontainers.image.vendor="Mattermost"       org.opencontainers.image.source="https://github.com/mattermost/mattermost-operator"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM