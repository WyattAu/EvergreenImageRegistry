FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/pawelmalak/flame/releases/download/v2.3.1/flame_2.3.1_linux_amd64.tar.gz" \
    -o /flame.tar.gz && \
    tar -xzf /flame.tar.gz -C / && rm /flame.tar.gz && chmod +x /flame 2>/dev/null || true
RUN strip /flame 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app/data /var/log/flame /var/cache/flame

FROM scratch
COPY --from=downloader /flame /flame 2>/dev/null || true
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/flame /var/log/flame
COPY --from=builder /var/cache/flame /var/cache/flame
USER 65532:65532
WORKDIR /app
EXPOSE 5005
ENTRYPOINT ["/flame"]
LABEL org.opencontainers.image.title="flame" \
      org.opencontainers.image.description="Flame - Self-hosted start page" \
      org.opencontainers.image.vendor="pawelmalak" \
      org.opencontainers.image.source="https://github.com/pawelmalak/flame" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM