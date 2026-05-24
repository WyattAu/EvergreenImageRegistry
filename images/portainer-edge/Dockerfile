ARG VERSION=2.39.2
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM portainer/agent:2.39.2@sha256:6c1b28b6dc1f785b055fa00e3f3d5fb43ff93910091384cecfb11bcda36e9f39 AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /var/log/portainer-edge /var/cache/portainer-edge 2>/dev/null || true


FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=upstream /agent_edge /portainer-edge-agent
COPY --from=builder /app /app
COPY --from=builder /var/log/portainer-edge /var/log/portainer-edge
COPY --from=builder /var/cache/portainer-edge /var/cache/portainer-edge

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="portainer-edge"       org.opencontainers.image.description="Portainer Edge Agent"       org.opencontainers.image.vendor="Portainer"       org.opencontainers.image.source="https://github.com/portainer/agent"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="latest"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/portainer-edge-agent"]

CMD ["--help"]
