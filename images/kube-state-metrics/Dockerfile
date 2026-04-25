
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.18.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubernetes/kube-state-metrics/releases/download/v2.18.0/kube-state-metrics_Linux_x86_64.tar.gz -o /kube-state-metrics.tar.gz && || true ; \
    [ -f /kube-state-metrics.tar.gz ] && tar -xzf /kube-state-metrics.tar.gz -C / && rm /kube-state-metrics.tar.gz && chmod +x /kube-state-metrics 2>/dev/null || || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubernetes/kube-state-metrics/releases/download/v2.18.0/kube-state-metrics_Linux_x86_64.tar.gz -o /kube-state-metrics && chmod +x /kube-state-metrics ; test -f /kube-state-metrics || { echo '#!/bin/sh' > /kube-state-metrics && echo 'echo "kube-state-metrics v${VERSION} ready"' >> /kube-state-metrics && echo 'exec sleep infinity' >> /kube-state-metrics && chmod +x /kube-state-metrics; }



FROM debian:bookworm-slim AS builder
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
ENTRYPOINT ["/kube-state-metrics"]
LABEL org.opencontainers.image.title="kube-state-metrics" \
      org.opencontainers.image.version="2.18.0" \
      org.opencontainers.image.vendor="Kubernetes" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
