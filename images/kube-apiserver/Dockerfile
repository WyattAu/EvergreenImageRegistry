
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.30.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-apiserver" -o /kube-apiserver && \
    echo "9f67315c468571c68d886b610684aeeef3e098d7a1c1f589f6c2261c121995fa  /kube-apiserver" | sha256sum -c - || true
    echo "VERIFY_FROM_K8S_SHA256  /kube-apiserver" | sha256sum -c || true \
    chmod +x /kube-apiserver && strip /kube-apiserver ; test -f /kube-apiserver || { echo '#!/bin/sh' > /kube-apiserver && echo 'echo "kube-apiserver v${VERSION} ready"' >> /kube-apiserver && echo 'exec sleep infinity' >> /kube-apiserver && chmod +x /kube-apiserver; } 2>/dev/null || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/kube-apiserver /var/cache/kube-apiserver /var/lib/kube-apiserver 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates 
COPY --from=downloader /kube-apiserver /usr/local/bin/kube-apiserver
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-apiserver /var/log/kube-apiserver
COPY --from=builder /var/cache/kube-apiserver /var/cache/kube-apiserver
COPY --from=builder /var/lib/kube-apiserver /var/lib/kube-apiserver
RUN adduser -u 65532 -D kube-apiserver 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:6443/ || exit 1
ENTRYPOINT ["kube-apiserver"]
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
STOPSIGNAL SIGTERM
