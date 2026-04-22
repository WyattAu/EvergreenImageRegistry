ARG VERSION=RELEASE.2025-04-08T16-46-15Z
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dl.min.io/client/mc/release/linux-amd64/mc" -o /mc && chmod +x /mc

FROM scratch
COPY --from=downloader /mc /mc
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 0
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/mc", "--version"]
ENTRYPOINT ["/mc"]
LABEL org.opencontainers.image.title="mc" \
      org.opencontainers.image.version="RELEASE.2025-04-08T16-46-15Z" \
      org.opencontainers.image.vendor="MinIO" \
      org.opencontainers.image.source="https://github.com/minio/mc" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
