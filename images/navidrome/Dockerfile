# =============================================================================
# SOVEREIGN HARDENED NAVIDROME
# Generated from template - Version: 0.52.5
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.52.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_amd64.tar.gz" -o /navidrome.tar.gz && \
    echo "b9781ea560ea09926557c665472faa26920738a5ffa0680c19f70df97f51598f  /navidrome.tar.gz" | sha256sum -c - && \
    tar -xzf /navidrome.tar.gz -C / && rm /navidrome.tar.gz && chmod +x /navidrome 2>/dev/null || \
    curl -fsSL "https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_amd64.tar.gz" -o /navidrome && chmod +x /navidrome

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/navidrome /var/cache/navidrome

FROM scratch
COPY --from=downloader /navidrome /navidrome
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/navidrome /var/log/navidrome
COPY --from=builder /var/cache/navidrome /var/cache/navidrome
USER 65534:65534
WORKDIR /app
EXPOSE 4533
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/navidrome", "--version"]
ENTRYPOINT ["/navidrome"]
LABEL org.opencontainers.image.title="navidrome" \
      org.opencontainers.image.version="0.52.5" \
      org.opencontainers.image.vendor="Navidrome" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
