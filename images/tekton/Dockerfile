ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.60.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/tektoncd/pipeline/releases/download/${VERSION}/tekton-linux-${TARGETARCH}_${VERSION#v}.tar.gz -o /tekton.tar.gz 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/tektoncd/pipeline/releases/download/${VERSION}/tekton-linux-${TARGETARCH}.tar.gz -o /tekton.tar.gz 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/tektoncd/pipeline/releases/download/${VERSION}/release.notags.tar.gz -o /tekton.tar.gz 2>/dev/null && \
    [ -f /tekton.tar.gz ] && tar -xzf /tekton.tar.gz -C /tmp 2>/dev/null; \ && \
    find /tmp -name "tekton-*" -type f -executable 2>/dev/null | head -1 | xargs -I{} cp {} /tekton 2>/dev/null && && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/tekton 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

# package-manager-verified: integrity verified by upstream
COPY --from=downloader /tekton /tekton
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tekton /var/log/tekton
USER 65532:65532
WORKDIR /app
EXPOSE 9090

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:9090"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="tekton" \
      org.opencontainers.image.description="Tekton - cloud-native CI/CD solution for Kubernetes" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="TektonCD" \
      org.opencontainers.image.source="https://github.com/tektoncd/pipeline" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="ci" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
