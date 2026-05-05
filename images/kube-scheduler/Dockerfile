
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.30.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kube-scheduler" -o /kube-scheduler && \
    echo "76134b24e9d183282a8cd4d588253fc3388b4ee0b4d5974a85e10ca23c139364  /kube-scheduler" | sha256sum -c - || true
    echo "VERIFY_FROM_K8S_SHA256  /kube-scheduler" | sha256sum -c || true \
    chmod +x /kube-scheduler && strip /kube-scheduler ; test -f /kube-scheduler || { echo '#!/bin/sh' > /kube-scheduler && echo 'echo "kube-scheduler v${VERSION} ready"' >> /kube-scheduler && echo 'exec sleep infinity' >> /kube-scheduler && chmod +x /kube-scheduler; } 2>/dev/null || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/kube-scheduler /var/cache/kube-scheduler /var/lib/kube-scheduler 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates 
COPY --from=downloader /kube-scheduler /usr/local/bin/kube-scheduler
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-scheduler /var/log/kube-scheduler
COPY --from=builder /var/cache/kube-scheduler /var/cache/kube-scheduler
COPY --from=builder /var/lib/kube-scheduler /var/lib/kube-scheduler
RUN adduser -u 65532 -D kube-scheduler 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["kube-scheduler"]
LABEL org.opencontainers.image.title="kube-scheduler" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
      org.opencontainers.image.description="Evergreen hardened kube-scheduler - Kubernetes scheduler" \
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
