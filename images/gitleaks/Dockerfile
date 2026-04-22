FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/gitleaks/gitleaks/releases/download/v8.21.2/gitleaks_8.21.2_linux_x64.tar.gz" -o /gitleaks_8.21.2_linux_x64.tar.gz &&     tar -xzf /gitleaks_8.21.2_linux_x64.tar.gz -C / && rm /gitleaks_8.21.2_linux_x64.tar.gz && chmod +x /gitleaks
RUN strip /gitleaks 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/gitleaks /var/cache/gitleaks

FROM scratch
COPY --from=downloader /gitleaks /gitleaks
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/gitleaks /var/log/gitleaks
COPY --from=builder /var/cache/gitleaks /var/cache/gitleaks
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/gitleaks", "--version"]
ENTRYPOINT ["/gitleaks"]
LABEL org.opencontainers.image.title="gitleaks"       org.opencontainers.image.description="Gitleaks - secret scanner"       org.opencontainers.image.vendor="gitleaks"       org.opencontainers.image.source="https://github.com/gitleaks/gitleaks"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
