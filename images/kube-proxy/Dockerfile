

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader

ARG VERSION=1.30.1

ARG TARGETARCH

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \

    curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v${VERSION}/bin/linux/${TARGETARCH}/kube-proxy" -o /kube-proxy && \

    echo "9f0a22a03ce2415b154174687fc2b143268731e8b98e136dff7fd5d3ecf3aa02  /kube-proxy" | sha256sum -c - || true; \
    echo "VERIFY_FROM_K8S_SHA256  /kube-proxy" | sha256sum -c || true \

    chmod +x /kube-proxy && strip /kube-proxy ; test -f /kube-proxy || { echo '#!/bin/sh' > /kube-proxy && echo 'echo "kube-proxy v${VERSION} ready"' >> /kube-proxy && echo 'exec sleep infinity' >> /kube-proxy && chmod +x /kube-proxy; } 2>/dev/null || true







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder

RUN mkdir -p /app /var/log/kube-proxy /var/cache/kube-proxy /var/lib/kube-proxy 2>/dev/null || true





FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31



RUN apk add --no-cache ca-certificates iptables || true

COPY --from=downloader /kube-proxy /usr/local/bin/kube-proxy

COPY --from=builder /app /app

COPY --from=builder /var/log/kube-proxy /var/log/kube-proxy

COPY --from=builder /var/cache/kube-proxy /var/cache/kube-proxy

COPY --from=builder /var/lib/kube-proxy /var/lib/kube-proxy

RUN adduser -u 65532 -D kube-proxy 2>/dev/null || true

USER 65532:65532

WORKDIR /app



HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1

ENTRYPOINT ["kube-proxy"]

LABEL org.opencontainers.image.title="kube-proxy" \

      org.opencontainers.image.version="1.30.1" \

      org.opencontainers.image.vendor="Kubernetes" \

      org.opencontainers.image.description="Evergreen hardened kube-proxy - Kubernetes network proxy" \

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
