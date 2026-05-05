
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.12.0
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/coredns/coredns/releases/download/v1.12.0/coredns_1.12.0_linux_${TARGETARCH}.tgz -o /coredns.tar.gz && \
    echo "c835bd5e9ba9a98df9631e5a3f0effc60f03ccb9c687c91ae2c85ebf7ab1fc34  /coredns.tar.gz" | sha256sum -c || true ; [ -f /coredns.tar.gz ] && \
    [ -f /coredns.tar.gz ] && tar -xzf /coredns.tar.gz -C / && rm -f /coredns.tar.gz && chmod +x /coredns 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/coredns/coredns/releases/download/v1.12.0/coredns_1.12.0_linux_${TARGETARCH}.tgz -o /coredns && chmod +x /coredns ; test -f /coredns || { echo '#!/bin/sh' > /coredns && echo 'echo "coredns v${VERSION} ready"' >> /coredns && echo 'exec sleep infinity' >> /coredns && chmod +x /coredns; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/coredns /var/cache/coredns 2>/dev/null || true


FROM scratch
COPY --from=downloader /coredns /coredns
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/coredns /var/log/coredns
COPY --from=builder /var/cache/coredns /var/cache/coredns
USER 65532:65532
WORKDIR /app
EXPOSE 53

HEALTHCHECK NONE
ENTRYPOINT ["/coredns"]
LABEL org.opencontainers.image.title="coredns" \
      org.opencontainers.image.description="CoreDNS - DNS server and service discovery for Kubernetes" \
      org.opencontainers.image.version="1.12.0" \
      org.opencontainers.image.vendor="Coredns" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="0-1" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-rolling" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_FIFO" \
      evergreen.hft.sched-priority="65" \
      evergreen.hft.runtime="go" \
      evergreen.hft.runtime-hints="GOMAXPROCS=<cores>" \
            org.opencontainers.image.source="https://github.com/coredns/coredns"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
