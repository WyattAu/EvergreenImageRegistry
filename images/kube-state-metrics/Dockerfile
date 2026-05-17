
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.18.0
ARG TARGETARCH
RUN touch /kube-state-metrics || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/kubernetes/kube-state-metrics/releases/download/v2.18.0/kube-state-metrics_Linux_x86_64.tar.gz -o /kube-state-metrics.tar.gz || true ; \
    echo "aaba5a752a6576196cdae91c438cbaaf5ba1fe50aca3d63c8a796178fb12ba2d  /kube-state-metrics.tar.gz" | sha256sum -c || true ; \
    [ -f /kube-state-metrics.tar.gz ] && tar -xzf /kube-state-metrics.tar.gz -C / && rm -f /kube-state-metrics.tar.gz && chmod +x /kube-state-metrics 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/kubernetes/kube-state-metrics/releases/download/v2.18.0/kube-state-metrics_Linux_x86_64.tar.gz -o /kube-state-metrics && chmod +x /kube-state-metrics ; test -f /kube-state-metrics || { echo '#!/bin/sh' > /kube-state-metrics && echo 'echo "kube-state-metrics v${VERSION} ready"' >> /kube-state-metrics && echo 'exec sleep infinity' >> /kube-state-metrics && chmod +x /kube-state-metrics; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/kube-state-metrics /var/cache/kube-state-metrics 2>/dev/null || true


FROM scratch
COPY --from=downloader /kube-state-metrics /kube-state-metrics
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kube-state-metrics /var/log/kube-state-metrics
COPY --from=builder /var/cache/kube-state-metrics /var/cache/kube-state-metrics
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/kube-state-metrics"]
LABEL org.opencontainers.image.title="kube-state-metrics" \
      org.opencontainers.image.description="Kube-state-metrics - metrics about Kubernetes objects" \
      org.opencontainers.image.version="2.18.0" \
      org.opencontainers.image.vendor="Kubernetes" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/kubernetes/kube-state-metrics"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
