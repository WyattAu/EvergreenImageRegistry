FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/trufflesecurity/trufflehog/releases/download/v3.82.2/trufflehog_3.82.2_linux_amd64.tar.gz" -o /trufflehog_3.82.2_linux_amd64.tar.gz &&     tar -xzf /trufflehog_3.82.2_linux_amd64.tar.gz -C / && rm /trufflehog_3.82.2_linux_amd64.tar.gz && chmod +x /trufflehog
RUN strip /trufflehog 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/truffelsh /var/cache/truffelsh

FROM scratch
COPY --from=downloader /trufflehog /trufflehog
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/truffelsh /var/log/truffelsh
COPY --from=builder /var/cache/truffelsh /var/cache/truffelsh
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="truffelsh"       org.opencontainers.image.description="TruffleHog - secret scanner (alias)"       org.opencontainers.image.vendor="trufflesecurity"       org.opencontainers.image.source="https://github.com/trufflesecurity/trufflehog"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM