FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/anchore/syft/releases/download/v1.11.0/syft_1.11.0_linux_amd64.tar.gz" -o /syft_1.11.0_linux_amd64.tar.gz &&     tar -xzf /syft_1.11.0_linux_amd64.tar.gz -C / && rm /syft_1.11.0_linux_amd64.tar.gz && chmod +x /syft
RUN strip /syft 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/syft-alpine /var/cache/syft-alpine

FROM scratch
COPY --from=downloader /syft /syft
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/syft-alpine /var/log/syft-alpine
COPY --from=builder /var/cache/syft-alpine /var/cache/syft-alpine
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/syft", "--version"]
ENTRYPOINT ["/syft"]
LABEL org.opencontainers.image.title="syft-alpine"       org.opencontainers.image.description="Syft - SBOM scanner (no Alpine)"       org.opencontainers.image.vendor="Anchore"       org.opencontainers.image.source="https://github.com/anchore/syft"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
