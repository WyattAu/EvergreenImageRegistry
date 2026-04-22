ARG VERSION=4.5.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/pydio/cells/releases/download/v4.5.0/cells-4.5.0-linux-amd64" -o /cells-agent && chmod +x /cells-agent

FROM scratch
COPY --from=downloader /cells-agent /cells-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 8081
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/cells-agent", "--version"]
ENTRYPOINT ["/cells-agent"]
LABEL org.opencontainers.image.title="pydio-agent" \
      org.opencontainers.image.version="4.5.0" \
      org.opencontainers.image.vendor="Pydio" \
      org.opencontainers.image.source="https://github.com/pydio/cells" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
