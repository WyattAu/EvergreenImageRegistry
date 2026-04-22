ARG VERSION=0.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/emuell/resticbrowser/releases/download/v0.3.0/resticbrowser-linux-amd64" -o /resticbrowser && chmod +x /resticbrowser

FROM scratch
COPY --from=downloader /resticbrowser /resticbrowser
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 9876
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/resticbrowser", "--version"]
ENTRYPOINT ["/resticbrowser"]
LABEL org.opencontainers.image.title="resticbrowser" \
      org.opencontainers.image.version="0.3.0" \
      org.opencontainers.image.vendor="ResticBrowser" \
      org.opencontainers.image.source="https://github.com/emuell/resticbrowser" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
