FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/clonezilla/keynuker/releases/download/v0.1.0/keynuker_0.1.0_linux_amd64" -o /keynuker && chmod +x /keynuker && strip /keynuker

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/keynuker /var/cache/keynuker

FROM scratch
COPY --from=downloader /keynuker /keynuker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/keynuker /var/log/keynuker
COPY --from=builder /var/cache/keynuker /var/cache/keynuker
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="keynuker"       org.opencontainers.image.description="KeyNuker - key detection"       org.opencontainers.image.vendor="clonezilla"       org.opencontainers.image.source="https://github.com/clonezilla/keynuker"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM