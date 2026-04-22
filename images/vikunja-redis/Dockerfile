ARG VERSION=v0.24.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/go-vikunja/vikunja/releases/download/v0.24.1/vikunja-v0.24.1-linux-amd64" -o /vikunja && chmod +x /vikunja

FROM scratch
COPY --from=downloader /vikunja /vikunja
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /app
EXPOSE 3456
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/vikunja", "--version"]
ENTRYPOINT ["/vikunja"]
CMD ["--config", "/app/config.yml"]
LABEL org.opencontainers.image.title="vikunja-redis" \
      org.opencontainers.image.version="v0.24.1" \
      org.opencontainers.image.vendor="Vikunja" \
      org.opencontainers.image.source="https://github.com/go-vikunja/vikunja" \
      org.opencontainers.image.description="Vikunja API with Redis backend configuration" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
