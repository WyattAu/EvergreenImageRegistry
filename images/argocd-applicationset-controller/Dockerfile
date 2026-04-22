# =============================================================================
# SOVEREIGN HARDENED ARGOCD-APPLICATIONSET-CONTROLLER
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# =============================================================================

ARG VERSION=2.14.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl="7.88.1-*" ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/argoproj/argo-cd/releases/download/v2.14.0/argocd-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/argocd-applicationset-controller
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534:65534
WORKDIR /app
EXPOSE 8083
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/usr/local/bin/argocd-applicationset-controller", "--version"]
ENTRYPOINT ["/usr/local/bin/argocd-applicationset-controller"]
LABEL org.opencontainers.image.title="argocd-applicationset-controller"       org.opencontainers.image.description="ArgoCD ApplicationSet Controller - generates ArgoCD applications from templates"       org.opencontainers.image.version="2.14.0"       org.opencontainers.image.vendor="Argo Project"       org.opencontainers.image.source="https://github.com/argoproj/argo-cd"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
