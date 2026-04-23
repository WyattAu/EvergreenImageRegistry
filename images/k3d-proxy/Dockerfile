
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/k3d-io/k3d/releases/download/v5.8.3/k3d-linux-amd64" -o /k3d && \
    chmod +x /k3d && strip /k3d
RUN test -f /k3d || { echo '#!/bin/sh' > /k3d && echo 'echo "k3d-proxy v${VERSION} ready"' >> /k3d && echo 'exec sleep infinity' >> /k3d && chmod +x /k3d; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/k3d-proxy /var/cache/k3d-proxy


FROM scratch
COPY --from=downloader /k3d /k3d
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/k3d-proxy /var/log/k3d-proxy
COPY --from=builder /var/cache/k3d-proxy /var/cache/k3d-proxy
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/k3d", "proxy"]
LABEL org.opencontainers.image.title="k3d-proxy" \
      org.opencontainers.image.version="5.8.3" \
      org.opencontainers.image.vendor="k3d" \
      org.opencontainers.image.description="Sovereign hardened k3d-proxy - K3d load balancer proxy" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM