FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/portainer/agent/releases/download/v2.21.4/portainer-agent-linux-amd64" -o /portainer-agent-linux-amd64 &&     tar -xzf /portainer-agent-linux-amd64 -C / && rm /portainer-agent-linux-amd64 && chmod +x /portainer-agent
RUN strip /portainer-agent 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/portainer-agent /var/cache/portainer-agent

FROM scratch
COPY --from=downloader /portainer-agent /portainer-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/portainer-agent /var/log/portainer-agent
COPY --from=builder /var/cache/portainer-agent /var/cache/portainer-agent
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/portainer-agent", "--version"]
ENTRYPOINT ["/portainer-agent"]
LABEL org.opencontainers.image.title="portainer-agent"       org.opencontainers.image.description="Portainer Agent for Docker"       org.opencontainers.image.vendor="Portainer"       org.opencontainers.image.source="https://github.com/portainer/agent"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
