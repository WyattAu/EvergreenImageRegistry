ARG VERSION=2.8.6
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/fluxcd/flux2/releases/download/v2.8.6/flux_2.8.6_linux_amd64.tar.gz" -o /flux.tar.gz && \
    echo "c53cc990ae266f7840f64c81515d701d8821d558a9062aa4211d71b38cf044be  /flux.tar.gz" | sha256sum -c - && \
    tar -xzf /flux.tar.gz -C / && rm /flux.tar.gz && chmod +x /flux && strip /flux

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/flux /var/cache/flux

FROM scratch
COPY --from=downloader /flux /flux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/flux /var/log/flux
COPY --from=builder /var/cache/flux /var/cache/flux
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/flux", "version"]
ENTRYPOINT ["/flux"]
LABEL org.opencontainers.image.title="flux2" \
      org.opencontainers.image.version="2.8.6" \
      org.opencontainers.image.vendor="Flux CD" \
      org.opencontainers.image.description="Sovereign hardened flux2 - GitOps toolkit" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"
