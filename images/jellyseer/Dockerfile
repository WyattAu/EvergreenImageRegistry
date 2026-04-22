ARG VERSION=v2.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Fallenbagel/jellyseerr/releases/download/v2.3.0/jellyseerr_2.3.0_linux_amd64.tar.gz" -o /jellyseerr && chmod +x /jellyseerr

FROM scratch
COPY --from=downloader /jellyseerr /jellyseerr
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 5055
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/jellyseerr", "--version"]
ENTRYPOINT ["/jellyseerr"]
LABEL org.opencontainers.image.title="jellyseer" \
      org.opencontainers.image.version="v2.3.0" \
      org.opencontainers.image.vendor="Jellyseerr" \
      org.opencontainers.image.source="https://github.com/Fallenbagel/jellyseerr" \
      sovereign.image.tier="2" \
      sovereign.image.category="media-streaming" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
