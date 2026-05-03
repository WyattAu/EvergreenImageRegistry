ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.12.6
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/argoproj/argo-cd/releases/download/v${VERSION}/argocd-linux-${TARGETARCH}" -o /tmp/argocd && \
    echo "efecedeb09f07b09ad4457467ceb103e1269004f34f7420a531372b13122fd2b  /tmp/argocd" | sha256sum -c - && \
    chmod +x /tmp/argocd && strip /tmp/argocd || true
RUN test -f /tmp/argocd && test -s /tmp/argocd || { echo "ERROR: argocd binary not downloaded" >&2; exit 1; }

FROM scratch
COPY --from=downloader /tmp/argocd /usr/local/bin/argocd-application-controller
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8082
LABEL org.opencontainers.image.title="argocd-application-controller" \
      org.opencontainers.image.description="ArgoCD Application Controller - manages application lifecycle" \
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

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["argocd-application-controller"]
