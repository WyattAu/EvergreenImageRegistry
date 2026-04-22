ARG VERSION=v0.4.29
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mickael-kerjean/filestash/releases/download/v0.4.29/filestash-linux-amd64" -o /filestash && chmod +x /filestash

FROM scratch
COPY --from=downloader /filestash /filestash
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 8334
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/filestash", "--version"]
ENTRYPOINT ["/filestash"]
LABEL org.opencontainers.image.title="filestash" \
      org.opencontainers.image.version="v0.4.29" \
      org.opencontainers.image.vendor="Filestash" \
      org.opencontainers.image.source="https://github.com/mickael-kerjean/filestash" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
