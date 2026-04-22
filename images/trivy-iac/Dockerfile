FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/aquasecurity/trivy/releases/download/v0.58.2/trivy_0.58.2_linux-amd64.tar.gz" -o /trivy_0.58.2_linux-amd64.tar.gz &&     tar -xzf /trivy_0.58.2_linux-amd64.tar.gz -C / && rm /trivy_0.58.2_linux-amd64.tar.gz && chmod +x /trivy
RUN strip /trivy 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/trivy-iac /var/cache/trivy-iac

FROM debian:bookworm-slim
COPY --from=downloader /trivy /usr/local/bin/trivy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin trivy-iac 2>/dev/null || true &&     chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["trivy", "--version"]
ENTRYPOINT ["trivy"]
LABEL org.opencontainers.image.title="trivy-iac"       org.opencontainers.image.description="Trivy - IaC scanner"       org.opencontainers.image.vendor="Aqua Security"       org.opencontainers.image.source="https://github.com/aquasecurity/trivy"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
