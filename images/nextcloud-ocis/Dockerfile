ARG VERSION=v5.0.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/nextcloud/ocis/releases/download/v5.0.1/ocis-5.0.1-linux-amd64" -o /nextcloud-ocis && chmod +x /nextcloud-ocis

FROM scratch
COPY --from=downloader /nextcloud-ocis /nextcloud-ocis
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 9200
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/nextcloud-ocis", "--version"]
ENTRYPOINT ["/nextcloud-ocis"]
LABEL org.opencontainers.image.title="nextcloud-ocis" \
      org.opencontainers.image.version="v5.0.1" \
      org.opencontainers.image.vendor="Nextcloud" \
      org.opencontainers.image.source="https://github.com/nextcloud/ocis" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
