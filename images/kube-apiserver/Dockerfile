







ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG VERSION=1.30.1







ARG TARGETARCH







RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v${VERSION}/bin/linux/${TARGETARCH}/kube-apiserver" -o /kube-apiserver && \
    echo "9f67315c468571c68d886b610684aeeef3e098d7a1c1f589f6c2261c121995fa  /kube-apiserver" | sha256sum -c; \
    echo "VERIFY_FROM_K8S_SHA256  /kube-apiserver" | sha256sum -c ; \
    chmod +x /kube-apiserver && strip /kube-apiserver && { echo "Binary not available - download failed" >&2; exit 1; }































FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /app /var/log/kube-apiserver /var/cache/kube-apiserver /var/lib/kube-apiserver 2>/dev/null || true























FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim
















RUN apk add --no-cache ca-certificates







COPY --from=downloader /kube-apiserver /usr/local/bin/kube-apiserver







COPY --from=builder /app /app







COPY --from=builder /var/log/kube-apiserver /var/log/kube-apiserver







COPY --from=builder /var/cache/kube-apiserver /var/cache/kube-apiserver







COPY --from=builder /var/lib/kube-apiserver /var/lib/kube-apiserver







RUN adduser -u 65532 -D kube-apiserver 2>/dev/null || true







USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"







WORKDIR /app







EXPOSE 6443






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6443"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]







LABEL org.opencontainers.image.title="kube-apiserver" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Evergreen hardened kube-apiserver - Kubernetes API server" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="15s" \
            org.opencontainers.image.source="https://github.com/kubernetes/kubernetes"







LABEL evergreen.base.image="wolfi"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
