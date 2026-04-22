FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/anchore/grype/releases/download/v0.80.0/grype_0.80.0_linux_amd64.tar.gz" -o /grype_0.80.0_linux_amd64.tar.gz &&     tar -xzf /grype_0.80.0_linux_amd64.tar.gz -C / && rm /grype_0.80.0_linux_amd64.tar.gz && chmod +x /grype
RUN strip /grype 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/grype-alpine /var/cache/grype-alpine

FROM scratch
COPY --from=downloader /grype /grype
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/grype-alpine /var/log/grype-alpine
COPY --from=builder /var/cache/grype-alpine /var/cache/grype-alpine
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/grype", "--version"]
ENTRYPOINT ["/grype"]
LABEL org.opencontainers.image.title="grype-alpine"       org.opencontainers.image.description="Grype - vulnerability scanner (no Alpine)"       org.opencontainers.image.vendor="Anchore"       org.opencontainers.image.source="https://github.com/anchore/grype"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
