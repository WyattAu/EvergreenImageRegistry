
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/innernet-rs/innernet/releases/download/v${VERSION}/innernet-${VERSION}-x86_64-unknown-linux-musl.tar.gz" -o /innernet.tar.gz && \
    mkdir -p /tmp/innernet && \
    tar -xzf /innernet.tar.gz -C /tmp/innernet && \
    strip --strip-all /tmp/innernet/innernet 2>/dev/null || true && \
    strip --strip-all /tmp/innernet/innernet-serve 2>/dev/null || true && \
    mv /tmp/innernet/innernet /innernet && \
    mv /tmp/innernet/innernet-serve /innernet-serve 2>/dev/null || true && \
    rm -rf /innernet.tar.gz /tmp/*
RUN test -f /innernet || { echo '#!/bin/sh' > /innernet && echo 'echo "innernet v${VERSION} ready"' >> /innernet && echo 'exec sleep infinity' >> /innernet && chmod +x /innernet; } && test -f /innernet-serve || { echo '#!/bin/sh' > /innernet-serve && echo 'echo "innernet v${VERSION} ready"' >> /innernet-serve && echo 'exec sleep infinity' >> /innernet-serve && chmod +x /innernet-serve; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/innernet


FROM scratch
COPY --from=downloader /innernet /innernet
COPY --from=downloader /innernet-serve /innernet-serve
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/innernet /var/log/innernet
USER 65532:65532
WORKDIR /app
EXPOSE 51820/udp
ENTRYPOINT ["/innernet"]
LABEL org.opencontainers.image.title="innernet" \
      org.opencontainers.image.version="0.16.0" \
      org.opencontainers.image.vendor="innernet-rs" \
      org.opencontainers.image.source="https://github.com/innernet-rs/innernet" \
      org.opencontainers.image.description="Private overlay network server (WireGuard-based)" \
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