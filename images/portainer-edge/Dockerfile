FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/portainer/agent/releases/download/v2.21.4/portainer-agent-edge-linux-amd64" -o /portainer-agent-edge-linux-amd64 &&     tar -xzf /portainer-agent-edge-linux-amd64 -C / && rm /portainer-agent-edge-linux-amd64 && chmod +x /portainer-edge-agent
RUN strip /portainer-edge-agent 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/portainer-edge /var/cache/portainer-edge

FROM scratch
COPY --from=downloader /portainer-edge-agent /portainer-edge-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/portainer-edge /var/log/portainer-edge
COPY --from=builder /var/cache/portainer-edge /var/cache/portainer-edge
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/portainer-edge-agent", "--version"]
ENTRYPOINT ["/portainer-edge-agent"]
LABEL org.opencontainers.image.title="portainer-edge"       org.opencontainers.image.description="Portainer Edge Agent"       org.opencontainers.image.vendor="Portainer"       org.opencontainers.image.source="https://github.com/portainer/agent"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
