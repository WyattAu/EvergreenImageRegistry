# =============================================================================
# SOVEREIGN HARDENED PIPER
# Generated from template - Version: 1.2.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.2.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_amd64.tar.gz" -o /piper && chmod +x /piper

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/piper /var/cache/piper

FROM scratch
COPY --from=downloader /piper /piper
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/piper /var/log/piper
COPY --from=builder /var/cache/piper /var/cache/piper
USER 65534:65534
WORKDIR /app
EXPOSE 6666
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/piper", "--version"]
ENTRYPOINT ["/piper"]
LABEL org.opencontainers.image.title="piper" \
      org.opencontainers.image.version="1.2.0" \
      org.opencontainers.image.vendor="rhasspy/piper" \
      org.opencontainers.image.source="https://github.com/rhasspy/piper/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
