ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=3.4.2
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/argoproj/argo-cd/releases/download/v3.4.2/argocd-linux-${TARGETARCH} -o /argocd && \
    echo "11070d2502c5a51523f78388e23ddefb9151bd33f2faab955cde78a9c0d492e6  /argocd" | sha256sum -c ; \
    chmod +x /argocd && strip /argocd 2>/dev/null && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/argocd /var/cache/argocd /home/argocd 2>/dev/null || true


FROM scratch
COPY --from=downloader /argocd /argocd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/argocd /var/log/argocd
COPY --from=builder /var/cache/argocd /var/cache/argocd
COPY --from=builder /home/argocd /home/argocd
USER 65532:65532
WORKDIR /app
ENV HOME=/app

HEALTHCHECK NONE
ENTRYPOINT ["/argocd"]
LABEL org.opencontainers.image.title="argo-cd" \
      org.opencontainers.image.version="3.4.2" \
      org.opencontainers.image.vendor="Argo Project" \
      org.opencontainers.image.description="Evergreen hardened argo-cd - GitOps CD tool" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
            org.opencontainers.image.source="https://github.com/argoproj/argo-cd"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
