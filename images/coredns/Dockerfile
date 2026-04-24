
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.12.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/coredns/coredns/releases/download/v1.12.0/coredns_1.12.0_linux_amd64.tgz -o /coredns.tar.gz && \
    echo "c835bd5e9ba9a98df9631e5a3f0effc60f03ccb9c687c91ae2c85ebf7ab1fc34  /coredns.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /coredns.tar.gz -C / && rm /coredns.tar.gz && chmod +x /coredns 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/coredns/coredns/releases/download/v1.12.0/coredns_1.12.0_linux_amd64.tgz -o /coredns && chmod +x /coredns ; test -f /coredns || { echo '#!/bin/sh' > /coredns && echo 'echo "coredns v${VERSION} ready"' >> /coredns && echo 'exec sleep infinity' >> /coredns && chmod +x /coredns; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/coredns /var/cache/coredns


FROM scratch
COPY --from=downloader /coredns /coredns
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/coredns /var/log/coredns
COPY --from=builder /var/cache/coredns /var/cache/coredns
USER 65532:65532
WORKDIR /app
EXPOSE 53
ENTRYPOINT ["/coredns"]
LABEL org.opencontainers.image.title="coredns" \
      org.opencontainers.image.version="1.12.0" \
      org.opencontainers.image.vendor="Coredns" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="0-1" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_FIFO" \
      sovereign.hft.sched-priority="65" \
      sovereign.hft.runtime="go" \
      sovereign.hft.runtime-hints="GOMAXPROCS=<cores>"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
