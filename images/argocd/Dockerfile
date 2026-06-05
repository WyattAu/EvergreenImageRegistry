ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v0.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
COPY --from=shim /shim /shim

ARG TARGETARCH
ARG VERSION=2.12.6

RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/argoproj/argo-cd/releases/download/v${VERSION}/argocd-linux-${TARGETARCH}" -o /tmp/argocd && \
    echo "efecedeb09f07b09ad4457467ceb103e1269004f34f7420a531372b13122fd2b  /tmp/argocd" | sha256sum -c && \
    chmod +x /tmp/argocd && strip /tmp/argocd && \
    test -f /tmp/argocd

FROM scratch
COPY --from=downloader /tmp/argocd /usr/local/bin/argocd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL org.opencontainers.image.title="argocd" \
      org.opencontainers.image.description="ArgoCD CLI - declarative GitOps continuous delivery for Kubernetes" \
      org.opencontainers.image.version="2.12.6" \
      org.opencontainers.image.vendor="Argo Project" \
      org.opencontainers.image.source="https://github.com/argoproj/argo-cd" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
