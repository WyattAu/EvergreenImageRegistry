ARG VERSION=v6.0.4
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/minio/operator/releases/download/v6.0.4/minio-operator_linux_amd64" -o /minio-operator && chmod +x /minio-operator

FROM scratch
COPY --from=downloader /minio-operator /minio-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 4455
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/minio-operator", "--version"]
ENTRYPOINT ["/minio-operator"]
LABEL org.opencontainers.image.title="minio-operator" \
      org.opencontainers.image.version="v6.0.4" \
      org.opencontainers.image.vendor="MinIO" \
      org.opencontainers.image.source="https://github.com/minio/operator" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
