# =============================================================================
# SOVEREIGN HARDENED AUTHELIA
# Generated from template - Version: 4.38.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.38.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/authelia/authelia/releases/download/v4.38.0/authelia_4.38.0_linux_amd64.tar.gz" -o /authelia.tar.gz && \
    tar -xzf /authelia.tar.gz -C / && rm /authelia.tar.gz && chmod +x /authelia 2>/dev/null || \
    curl -fsSL "https://github.com/authelia/authelia/releases/download/v4.38.0/authelia_4.38.0_linux_amd64.tar.gz" -o /authelia && chmod +x /authelia

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/authelia /var/cache/authelia

FROM scratch
COPY --from=downloader /authelia /authelia
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/authelia /var/log/authelia
COPY --from=builder /var/cache/authelia /var/cache/authelia
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/authelia", "version"]
ENTRYPOINT ["/authelia"]
LABEL org.opencontainers.image.title="authelia" \
      org.opencontainers.image.version="4.38.0" \
      org.opencontainers.image.vendor="Authelia" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
