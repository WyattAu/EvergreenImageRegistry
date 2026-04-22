ARG VERSION=3.8.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/cloudreve/Cloudreve/releases/download/3.8.3/cloudreve_3.8.3_linux_amd64.tar.gz" -o /cloudreve && chmod +x /cloudreve

FROM scratch
COPY --from=downloader /cloudreve /cloudreve
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 5212
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/cloudreve", "--version"]
ENTRYPOINT ["/cloudreve"]
LABEL org.opencontainers.image.title="cloudreve" \
      org.opencontainers.image.version="3.8.3" \
      org.opencontainers.image.vendor="Cloudreve" \
      org.opencontainers.image.source="https://github.com/cloudreve/Cloudreve" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
