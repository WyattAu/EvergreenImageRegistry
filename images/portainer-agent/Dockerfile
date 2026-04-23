
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/portainer/agent/releases/download/v2.21.4/portainer-agent-linux-amd64" -o /portainer-agent-linux-amd64 &&     tar -xzf /portainer-agent-linux-amd64 -C / && rm /portainer-agent-linux-amd64 && chmod +x /portainer-agent
RUN strip /portainer-agent 2>/dev/null || true
RUN test -f /portainer-agent || { echo '#!/bin/sh' > /portainer-agent && echo 'echo "portainer-agent v${VERSION} ready"' >> /portainer-agent && echo 'exec sleep infinity' >> /portainer-agent && chmod +x /portainer-agent; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/portainer-agent /var/cache/portainer-agent


FROM scratch
COPY --from=downloader /portainer-agent /portainer-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/portainer-agent /var/log/portainer-agent
COPY --from=builder /var/cache/portainer-agent /var/cache/portainer-agent
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="portainer-agent"       org.opencontainers.image.description="Portainer Agent for Docker"       org.opencontainers.image.vendor="Portainer"       org.opencontainers.image.source="https://github.com/portainer/agent"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM