ARG VERSION=v1.5.1

FROM gravitl/netmaker-ui:v1.5.1 AS upstream

FROM gcr.io/distroless/static-debian12@sha256:20bc6c0bc4d625a22a8fde3e55f6515709b32055ef8fb9cfbddaa06d1760f838
COPY --from=upstream /usr/share/nginx/html /www
USER 65532:65532
WORKDIR /www
EXPOSE 8080
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="netmaker-ui"       org.opencontainers.image.version="v1.5.1"       org.opencontainers.image.vendor="Gravitl"       org.opencontainers.image.source="https://github.com/gravitl/netmaker-ui"       sovereign.image.tier="1"       sovereign.image.category="networking"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.distrole="distroless"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="3s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="distroless"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
