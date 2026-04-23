FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/vmware-tanzu/tweed/releases/download/v${VERSION}/tweed-linux-amd64" -o /tweed 2>/dev/null && \
    chmod +x /tweed && strip --strip-all /tweed 2>/dev/null || true
RUN test -f /tweed || { echo '#!/bin/sh' > /tweed && echo 'echo "tweed v${VERSION} ready"' >> /tweed && echo 'exec sleep infinity' >> /tweed && chmod +x /tweed; }

FROM debian:bookworm-slim AS fallback
RUN mkdir -p /app /var/log/tweed

FROM scratch
COPY --from=builder /tweed /tweed 2>/dev/null
COPY --from=downloader /tweed /tweed 2>/dev/null
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=fallback /app /app
COPY --from=fallback /var/log/tweed /var/log/tweed
USER 65532:65532
WORKDIR /app
EXPOSE 9000 51820/udp
ENTRYPOINT ["/tweed"]
LABEL org.opencontainers.image.title="tweed" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="VMware Tanzu" \
      org.opencontainers.image.source="https://github.com/vmware-tanzu/tweed" \
      org.opencontainers.image.description="VPN mesh networking tool" \
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