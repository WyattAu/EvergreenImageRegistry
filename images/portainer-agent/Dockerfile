ARG VERSION=2.39.2
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM portainer/agent:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/portainer-agent /var/cache/portainer-agent 2>/dev/null || true


FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt || true
COPY --from=upstream /agent /portainer-agent || true
COPY --from=builder /app /app || true
COPY --from=builder /var/log/portainer-agent /var/log/portainer-agent || true
COPY --from=builder /var/cache/portainer-agent /var/cache/portainer-agent || true

WORKDIR /app

EXPOSE 9101

LABEL org.opencontainers.image.title="portainer-agent"       org.opencontainers.image.description="Portainer Agent for Docker"       org.opencontainers.image.vendor="Portainer"       org.opencontainers.image.source="https://github.com/portainer/agent"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
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
ENTRYPOINT ["/portainer-agent"]

CMD ["--help"]
