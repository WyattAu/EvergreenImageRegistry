FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/SelfhostedPro/Yacht/releases/download/v2.2.2/yacht_2.2.2_linux_amd64.tar.gz" -o /yacht_2.2.2_linux_amd64.tar.gz &&     tar -xzf /yacht_2.2.2_linux_amd64.tar.gz -C / && rm /yacht_2.2.2_linux_amd64.tar.gz && chmod +x /yacht
RUN strip /yacht 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/yacht /var/cache/yacht

FROM debian:bookworm-slim
COPY --from=downloader /yacht /usr/local/bin/yacht
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin yacht 2>/dev/null || true &&     chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["yacht", "--version"]
ENTRYPOINT ["yacht"]
LABEL org.opencontainers.image.title="yacht"       org.opencontainers.image.description="Yacht - Docker management UI"       org.opencontainers.image.vendor="SelfhostedPro"       org.opencontainers.image.source="https://github.com/SelfhostedPro/Yacht"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
