FROM debian:bookworm-slim AS downloader
ARG VERSION=2.12.6
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/argoproj/argo-cd/releases/download/v${VERSION}/argocd-linux-amd64" -o /tmp/argocd && \
    chmod +x /tmp/argocd && strip /tmp/argocd || true
RUN test -f /tmp/argocd && test -s /tmp/argocd || { echo "ERROR: argocd binary not downloaded" >&2; exit 1; }

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
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
ENTRYPOINT ["argocd"]
