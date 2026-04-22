FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/snyk/snyk/releases/download/v1.1295.0/snyk-linux" -o /snyk-alpine && chmod +x /snyk-alpine && strip /snyk-alpine

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/snyk-alpine /var/cache/snyk-alpine

FROM debian:bookworm-slim
COPY --from=downloader /snyk-alpine /usr/local/bin/snyk-alpine
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin snyk-alpine 2>/dev/null || true &&     chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["snyk-alpine", "--version"]
ENTRYPOINT ["snyk-alpine"]
LABEL org.opencontainers.image.title="snyk-alpine"       org.opencontainers.image.description="Snyk - security scanner (no Alpine)"       org.opencontainers.image.vendor="Snyk"       org.opencontainers.image.source="https://github.com/snyk/snyk"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
