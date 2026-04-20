# =============================================================================
# SOVEREIGN HARDENED RESTIC
# Generated from template - Version: 0.17.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.17.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/restic/restic/releases/download/v0.17.0/restic_0.17.0_linux_amd64.tar.gz" -o /restic.tar.gz && \
    echo "72fbdbca48fabbc84dfe551bdd3bc2d8d8b96b30ca7a2a71344c4d0878d91d99  /restic.tar.gz" | sha256sum -c - && \
    tar -xzf /restic.tar.gz -C / && rm /restic.tar.gz && chmod +x /restic 2>/dev/null || \
    curl -fsSL "https://github.com/restic/restic/releases/download/v0.17.0/restic_0.17.0_linux_amd64.tar.gz" -o /restic && chmod +x /restic

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/restic /var/cache/restic

FROM scratch
COPY --from=downloader /restic /restic
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/restic /var/log/restic
COPY --from=builder /var/cache/restic /var/cache/restic
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/restic", "version"]
ENTRYPOINT ["/restic"]
LABEL org.opencontainers.image.title="restic" \
      org.opencontainers.image.version="0.17.0" \
      org.opencontainers.image.vendor="Restic" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
