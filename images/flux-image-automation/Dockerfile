ARG APP_UID=65532
ARG APP_GID=65532

FROM ghcr.io/fluxcd/image-automation-controller:v1.1.3 AS upstream

FROM scratch
COPY --from=upstream /image-automation-controller /usr/local/bin/image-automation-controller
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/image-automation-controller"]
LABEL org.opencontainers.image.title="flux-image-automation" \
      org.opencontainers.image.description="Flux Image Automation Controller - automated container image updates for GitOps" \
      org.opencontainers.image.version="1.1.2" \
      org.opencontainers.image.vendor="Flux CD" \
      org.opencontainers.image.source="https://github.com/fluxcd/image-automation-controller" \
      evergreen.image.tier="2" \
      evergreen.image.category="gitops" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
