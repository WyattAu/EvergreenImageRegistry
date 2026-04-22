FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/aquasecurity/trivy/releases/download/v0.58.2/trivy_0.58.2_linux-amd64.tar.gz" -o /trivy_0.58.2_linux-amd64.tar.gz &&     tar -xzf /trivy_0.58.2_linux-amd64.tar.gz -C / && rm /trivy_0.58.2_linux-amd64.tar.gz && chmod +x /trivy
RUN strip /trivy 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/trivy-alpine /var/cache/trivy-alpine

FROM scratch
COPY --from=downloader /trivy /trivy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/trivy-alpine /var/log/trivy-alpine
COPY --from=builder /var/cache/trivy-alpine /var/cache/trivy-alpine
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/trivy", "--version"]
ENTRYPOINT ["/trivy"]
LABEL org.opencontainers.image.title="trivy-alpine"       org.opencontainers.image.description="Trivy - vulnerability scanner (no Alpine)"       org.opencontainers.image.vendor="Aqua Security"       org.opencontainers.image.source="https://github.com/aquasecurity/trivy"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
