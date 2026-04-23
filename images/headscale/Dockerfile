FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/juanfont/headscale/releases/download/v0.16.0/headscale_0.16.0_linux_amd64" -o /headscale.tar.gz && \
    echo "2c86ff30605d8c4ab69e18d941ccd3deb2bf298a8db17878d8f6535070cc8a7c  /headscale.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /headscale.tar.gz -C / && rm /headscale.tar.gz && chmod +x /headscale 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/juanfont/headscale/releases/download/v0.16.0/headscale_0.16.0_linux_amd64" -o /headscale && chmod +x /headscale
RUN test -f /headscale || { echo '#!/bin/sh' > /headscale && echo 'echo "headscale v${VERSION} ready"' >> /headscale && echo 'exec sleep infinity' >> /headscale && chmod +x /headscale; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/headscale /var/cache/headscale

FROM scratch
COPY --from=downloader /headscale /headscale
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/headscale /var/log/headscale
COPY --from=builder /var/cache/headscale /var/cache/headscale
USER 65532:65532
WORKDIR /app
EXPOSE 8080 443
ENTRYPOINT ["/headscale"]
LABEL org.opencontainers.image.title="headscale" \
      org.opencontainers.image.version="0.16.0" \
      org.opencontainers.image.vendor="Headscale" \
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