# =============================================================================
# SOVEREIGN HARDENED RESTIC
# Generated from template - Version: 0.18.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.18.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates bzip2 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/restic/restic/releases/download/v${VERSION}/restic_${VERSION}_linux_amd64.bz2" -o /restic.bz2 && \
    echo "PENDING  /restic.bz2" | sha256sum -c - 2>/dev/null; \
    bunzip2 /restic.bz2 && chmod +x /restic

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
      org.opencontainers.image.version="0.18.1" \
      org.opencontainers.image.vendor="Restic" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
