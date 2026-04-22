ARG VERSION=v2.32.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/filebrowser/filebrowser/releases/download/v2.32.0/linux-amd64-filebrowser.tar.gz" -o /filebrowser && chmod +x /filebrowser

FROM scratch
COPY --from=downloader /filebrowser /filebrowser
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/filebrowser", "--version"]
ENTRYPOINT ["/filebrowser"]
LABEL org.opencontainers.image.title="filebrowser" \
      org.opencontainers.image.version="v2.32.0" \
      org.opencontainers.image.vendor="FileBrowser" \
      org.opencontainers.image.source="https://github.com/filebrowser/filebrowser" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
