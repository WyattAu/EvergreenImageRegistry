# =============================================================================
# SOVEREIGN HARDENED FLUX-IMAGE-AUTOMATION
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=0.39.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/fluxcd/image-automation-controller/releases/download/v0.39.0/image-automation-controller-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/image-automation-controller
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/image-automation-controller", "--version"]
ENTRYPOINT ["/usr/local/bin/image-automation-controller"]
LABEL org.opencontainers.image.title="flux-image-automation"       org.opencontainers.image.description="Flux Image Automation - automated container image updates for GitOps"       org.opencontainers.image.version="0.39.0"       org.opencontainers.image.vendor="Flux CD"       org.opencontainers.image.source="https://github.com/fluxcd/image-automation-controller"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
