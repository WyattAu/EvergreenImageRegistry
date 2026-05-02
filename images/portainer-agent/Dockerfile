ARG VERSION=latest

FROM portainer/agent:${VERSION} AS upstream

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/portainer-agent /var/cache/portainer-agent 2>/dev/null || true


FROM scratch
COPY --from=upstream /agent /portainer-agent
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/portainer-agent /var/log/portainer-agent
COPY --from=builder /var/cache/portainer-agent /var/cache/portainer-agent

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="portainer-agent"       org.opencontainers.image.description="Portainer Agent for Docker"       org.opencontainers.image.vendor="Portainer"       org.opencontainers.image.source="https://github.com/portainer/agent"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/portainer-agent"]

CMD ["--help"]
