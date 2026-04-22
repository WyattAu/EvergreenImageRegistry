FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/jesseduffield/lazydocker/releases/download/v0.12.0/lazydocker_0.12.0_Linux_x86_64.tar.gz" -o /lazydocker_0.12.0_Linux_x86_64.tar.gz &&     tar -xzf /lazydocker_0.12.0_Linux_x86_64.tar.gz -C / && rm /lazydocker_0.12.0_Linux_x86_64.tar.gz && chmod +x /lazydocker
RUN strip /lazydocker 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/lazydocker-ui /var/cache/lazydocker-ui

FROM debian:bookworm-slim
COPY --from=downloader /lazydocker /usr/local/bin/lazydocker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin lazydocker-ui 2>/dev/null || true &&     chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["lazydocker", "--version"]
ENTRYPOINT ["lazydocker"]
LABEL org.opencontainers.image.title="lazydocker-ui"       org.opencontainers.image.description="Lazydocker - UI mode"       org.opencontainers.image.vendor="jesseduffield"       org.opencontainers.image.source="https://github.com/jesseduffield/lazydocker"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
