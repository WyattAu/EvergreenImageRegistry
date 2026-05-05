ARG VERSION=v1.5.1

FROM gravitl/netmaker-ui@sha256:e3cde240375ae137e037e8ec33d144441b70486f688c5a00cc2ab265812490e8 AS upstream

FROM gcr.io/distroless/static-debian12@sha256:20bc6c0bc4d625a22a8fde3e55f6515709b32055ef8fb9cfbddaa06d1760f838
COPY --from=upstream /usr/share/nginx/html /www
USER 65532:65532
WORKDIR /www
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="netmaker-ui"       org.opencontainers.image.version="v1.5.1"       org.opencontainers.image.vendor="Gravitl"       org.opencontainers.image.source="https://github.com/gravitl/netmaker-ui"       evergreen.image.tier="1"       evergreen.image.category="networking"       evergreen.image.status="functional"       evergreen.constraint.nonroot="true"       evergreen.constraint.distrole="distroless"       evergreen.hft.signal-handling="native"       evergreen.hft.shutdown-timeout="3s"       evergreen.hft.init-system="none"       evergreen.hft.startup-timeout="3000ms" \
org.opencontainers.image.description="netmaker-ui container image" \

LABEL evergreen.base.image="distroless"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
