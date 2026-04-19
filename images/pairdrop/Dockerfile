# =============================================================================
# SOVEREIGN HARDENED PAIRDROP
# Generated from template - Version: 1.6.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.6.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/schmich/pairdrop/releases/download/v1.6.0/pairdrop-1.6.0-linux-amd64.tar.gz" -o /pairdrop.tar.gz && \
    tar -xzf /pairdrop.tar.gz -C / && rm /pairdrop.tar.gz && chmod +x /pairdrop 2>/dev/null || \
    curl -fsSL "https://github.com/schmich/pairdrop/releases/download/v1.6.0/pairdrop-1.6.0-linux-amd64.tar.gz" -o /pairdrop && chmod +x /pairdrop

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/pairdrop /var/cache/pairdrop

FROM scratch
COPY --from=downloader /pairdrop /pairdrop
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pairdrop /var/log/pairdrop
COPY --from=builder /var/cache/pairdrop /var/cache/pairdrop
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/pairdrop", "--version"]
ENTRYPOINT ["/pairdrop"]
LABEL org.opencontainers.image.title="pairdrop" \
      org.opencontainers.image.version="1.6.0" \
      org.opencontainers.image.vendor="PairDrop" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
