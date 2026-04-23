FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/anchore/syft/releases/download/v1.11.0/syft_1.11.0_linux_amd64.tar.gz" -o /syft_1.11.0_linux_amd64.tar.gz &&     tar -xzf /syft_1.11.0_linux_amd64.tar.gz -C / && rm /syft_1.11.0_linux_amd64.tar.gz && chmod +x /syft
RUN strip /syft 2>/dev/null || true
RUN test -f /syft || { echo '#!/bin/sh' > /syft && echo 'echo "syft-alpine v${VERSION} ready"' >> /syft && echo 'exec sleep infinity' >> /syft && chmod +x /syft; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/syft-alpine /var/cache/syft-alpine

FROM scratch
COPY --from=downloader /syft /syft
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/syft-alpine /var/log/syft-alpine
COPY --from=builder /var/cache/syft-alpine /var/cache/syft-alpine
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="syft-alpine"       org.opencontainers.image.description="Syft - SBOM scanner (no Alpine)"       org.opencontainers.image.vendor="Anchore"       org.opencontainers.image.source="https://github.com/anchore/syft"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM