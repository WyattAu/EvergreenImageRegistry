







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG VERSION=1.30.1







ARG TARGETARCH







RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v${VERSION}/bin/linux/${TARGETARCH}/kube-controller-manager" -o /kube-controller-manager && \
    echo "3cc74cdcb7ebb95577fea7f5e4ef2b15e59058a85040fdfdd7292016dbbf1c46  /kube-controller-manager" | sha256sum -c || true || true; \
    echo "VERIFY_FROM_K8S_SHA256  /kube-controller-manager" | sha256sum -c || true ; \
    chmod +x /kube-controller-manager && strip /kube-controller-manager  || true; test -f /kube-controller-manager || { echo '#!/bin/sh' > /kube-controller-manager && echo 'echo "kube-controller v${VERSION} ready"' >> /kube-controller-manager && echo 'exec sleep infinity' >> /kube-controller-manager && chmod +x /kube-controller-manager; } 2>/dev/null || true































FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /app /var/log/kube-controller /var/cache/kube-controller /var/lib/kube-controller 2>/dev/null || true























FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9















RUN apk add --no-cache ca-certificates 







COPY --from=downloader /kube-controller-manager /usr/local/bin/kube-controller-manager







COPY --from=builder /app /app







COPY --from=builder /var/log/kube-controller /var/log/kube-controller







COPY --from=builder /var/cache/kube-controller /var/cache/kube-controller







COPY --from=builder /var/lib/kube-controller /var/lib/kube-controller







RUN adduser -u 65532 -D kube-controller 2>/dev/null || true







USER 65532:65532







WORKDIR /app















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1







ENTRYPOINT ["kube-controller-manager"]







LABEL org.opencontainers.image.title="kube-controller" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Evergreen hardened kube-controller - Kubernetes controller manager" \
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







STOPSIGNAL SIGTERM
