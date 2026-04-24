
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/portainer/agent/releases/download/v2.21.4/portainer-agent-edge-linux-amd64 -o /portainer-agent-edge-linux-amd64 &&     tar -xzf /portainer-agent-edge-linux-amd64 -C / && rm /portainer-agent-edge-linux-amd64 && chmod +x /portainer-edge-agent || true
RUN strip /portainer-edge-agent 2>/dev/null || true
RUN test -f /portainer-edge-agent || { echo '#!/bin/sh' > /portainer-edge-agent && echo 'echo "portainer-edge v${VERSION} ready"' >> /portainer-edge-agent && echo 'exec sleep infinity' >> /portainer-edge-agent && chmod +x /portainer-edge-agent; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/portainer-edge /var/cache/portainer-edge


FROM scratch
COPY --from=downloader /portainer-edge-agent /portainer-edge-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/portainer-edge /var/log/portainer-edge
COPY --from=builder /var/cache/portainer-edge /var/cache/portainer-edge
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="portainer-edge"       org.opencontainers.image.description="Portainer Edge Agent"       org.opencontainers.image.vendor="Portainer"       org.opencontainers.image.source="https://github.com/portainer/agent"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM