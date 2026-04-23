FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/argoproj/argo-cd/releases/download/v2.14.0/argocd-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary




FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/argocd-notifications
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 9001
LABEL org.opencontainers.image.title="argocd-notifications"       org.opencontainers.image.description="ArgoCD Notifications - notification controller for ArgoCD"       org.opencontainers.image.version="2.14.0"       org.opencontainers.image.vendor="Argo Project"       org.opencontainers.image.source="https://github.com/argoproj/argo-cd"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM