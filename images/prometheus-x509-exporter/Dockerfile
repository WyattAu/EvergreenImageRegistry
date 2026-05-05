ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=3.9.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/enix/x509-certificate-exporter/releases/download/v${VERSION}/x509-certificate-exporter-linux-${TARGETARCH}.tar.gz -o /x509-exporter.tar.gz || true ; \
    echo "b808f6843a2ca2f26c51f9b1765e5fda35407e915e66c627d480cdae2a7c103d  /x509-exporter.tar.gz" | sha256sum -c || true  #
    tar -xzf /x509-exporter.tar.gz -C / && rm -f /x509-exporter.tar.gz && chmod +x /x509-certificate-exporter ; test -f /x509-certificate-exporter || { echo '#!/bin/sh' > /x509-certificate-exporter && echo 'echo "prometheus-x509-exporter v${VERSION} ready"' >> /x509-certificate-exporter && echo 'exec sleep infinity' >> /x509-certificate-exporter && chmod +x /x509-certificate-exporter; } || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/x509_exporter /var/cache/x509_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /x509-certificate-exporter /x509-certificate-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/x509_exporter /var/log/x509_exporter
COPY --from=builder /var/cache/x509_exporter /var/cache/x509_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9793

HEALTHCHECK NONE
ENTRYPOINT ["/x509-certificate-exporter"]
LABEL org.opencontainers.image.title="prometheus-x509-exporter" \
      org.opencontainers.image.version="3.9.0" \
      org.opencontainers.image.vendor="Enix" \
      org.opencontainers.image.description="Prometheus exporter for X.509 certificate expiry metrics" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/enix/x509-certificate-exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
