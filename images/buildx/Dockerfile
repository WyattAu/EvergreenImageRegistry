ARG VERSION=v0.33.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/docker/buildx/releases/download/v0.33.0/buildx-v0.33.0.linux-amd64" -o /buildx && \
    echo "b1b5a38f78311cfed70a0e68096df0e9ed7dd1b1fcd09adbb117d74e3bad6f32  /buildx" | sha256sum -c - && \
    chmod +x /buildx && strip /buildx

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/buildx /var/cache/buildx

FROM scratch
COPY --from=downloader /buildx /buildx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/buildx /var/log/buildx
COPY --from=builder /var/cache/buildx /var/cache/buildx
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/buildx", "version"]
ENTRYPOINT ["/buildx"]
LABEL org.opencontainers.image.title="buildx" \
      org.opencontainers.image.version="0.33.0" \
      org.opencontainers.image.vendor="Docker" \
      org.opencontainers.image.description="Sovereign hardened buildx - Docker multi-platform build" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"
