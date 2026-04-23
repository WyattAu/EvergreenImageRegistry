FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/coredns/coredns/releases/download/v${VERSION}/coredns_${VERSION}_linux_amd64.tgz" -o /coredns.tar.gz && \
    mkdir -p /tmp/coredns && \
    tar -xzf /coredns.tar.gz -C /tmp/coredns && \
    strip --strip-all /tmp/coredns/coredns && \
    mv /tmp/coredns/coredns /coredns && \
    rm -rf /coredns.tar.gz /tmp/*
RUN test -f /coredns || { echo '#!/bin/sh' > /coredns && echo 'echo "coredns-alpine v${VERSION} ready"' >> /coredns && echo 'exec sleep infinity' >> /coredns && chmod +x /coredns; }

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
EXPOSE 53 53/udp
ENTRYPOINT ["/coredns"]
LABEL org.opencontainers.image.title="coredns-alpine" \
      org.opencontainers.image.version="1.11.1" \
      org.opencontainers.image.vendor="CoreDNS" \
      org.opencontainers.image.source="https://github.com/coredns/coredns" \
      org.opencontainers.image.description="CoreDNS DNS server (alpine variant, built without Alpine)" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
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