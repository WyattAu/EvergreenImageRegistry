ARG VERSION=v0.21.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/google/go-containerregistry/releases/download/v0.21.5/go-containerregistry_Linux_x86_64.tar.gz" -o /crane.tar.gz && \
    echo "05150194f251b96c58e0da5fafffe5e30bff26704211236b39a814ef733f9c36  /crane.tar.gz" | sha256sum -c - && \
    tar -xzf /crane.tar.gz -C / && rm /crane.tar.gz && chmod +x /crane && strip /crane

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/crane /var/cache/crane

FROM scratch
COPY --from=downloader /crane /crane
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/crane /var/log/crane
COPY --from=builder /var/cache/crane /var/cache/crane
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/crane", "version"]
ENTRYPOINT ["/crane"]
LABEL org.opencontainers.image.title="crane" \
      org.opencontainers.image.version="0.21.5" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.description="Sovereign hardened crane - container registry client" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"
