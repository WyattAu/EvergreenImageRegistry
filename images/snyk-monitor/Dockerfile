FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/snyk/snyk/releases/download/v1.1295.0/snyk-linux" -o /snyk-monitor && chmod +x /snyk-monitor && strip /snyk-monitor

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/snyk-monitor /var/cache/snyk-monitor

FROM debian:bookworm-slim
COPY --from=downloader /snyk-monitor /usr/local/bin/snyk-monitor
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin snyk-monitor 2>/dev/null || true &&     chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["snyk-monitor", "--version"]
ENTRYPOINT ["snyk-monitor"]
LABEL org.opencontainers.image.title="snyk-monitor"       org.opencontainers.image.description="Snyk - monitor mode"       org.opencontainers.image.vendor="Snyk"       org.opencontainers.image.source="https://github.com/snyk/snyk"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
