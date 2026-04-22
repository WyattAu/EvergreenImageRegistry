ARG VERSION=v5.8.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/k3d-io/k3d/releases/download/v5.8.3/k3d-linux-amd64" -o /k3d && \
    chmod +x /k3d && strip /k3d

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/k3d /var/cache/k3d

FROM scratch
COPY --from=downloader /k3d /k3d
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/k3d /var/log/k3d
COPY --from=builder /var/cache/k3d /var/cache/k3d
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/k3d", "version"]
ENTRYPOINT ["/k3d"]
LABEL org.opencontainers.image.title="k3d" \
      org.opencontainers.image.version="5.8.3" \
      org.opencontainers.image.vendor="k3d" \
      org.opencontainers.image.description="Sovereign hardened k3d - K3s in Docker" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
