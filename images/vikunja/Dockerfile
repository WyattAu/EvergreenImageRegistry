# =============================================================================
# SOVEREIGN HARDENED VIKUNJA
# Generated from template - Version: 2.3.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/go-vikunja/vikunja/releases/download/v2.3.0/vikunja-v2.3.0-linux-amd64-full.zip" -o /vikunja.tar.gz && \
    tar -xzf /vikunja.tar.gz -C / && rm /vikunja.tar.gz && chmod +x /vikunja 2>/dev/null || \
    curl -fsSL "https://github.com/go-vikunja/vikunja/releases/download/v2.3.0/vikunja-v2.3.0-linux-amd64-full.zip" -o /vikunja && chmod +x /vikunja

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/vikunja /var/cache/vikunja

FROM scratch
COPY --from=downloader /vikunja /vikunja
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vikunja /var/log/vikunja
COPY --from=builder /var/cache/vikunja /var/cache/vikunja
USER 65534:65534
WORKDIR /app
EXPOSE 3456
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/vikunja", "--version"]
ENTRYPOINT ["/vikunja"]
LABEL org.opencontainers.image.title="vikunja" \
      org.opencontainers.image.version="2.3.0" \
      org.opencontainers.image.vendor="Vikunja" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
