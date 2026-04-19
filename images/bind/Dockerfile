# =============================================================================
# SOVEREIGN HARDENED BIND
# Generated from template - Version: 9.18.24
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=9.18.24
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://ftp.isc.org/isc/bind9/9.18.24/bind-9.18.24.tar.gz" -o /named.tar.gz && \
    tar -xzf /named.tar.gz -C / && rm /named.tar.gz && chmod +x /named 2>/dev/null || \
    curl -fsSL "https://ftp.isc.org/isc/bind9/9.18.24/bind-9.18.24.tar.gz" -o /named && chmod +x /named

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/named /var/cache/named

FROM scratch
COPY --from=downloader /named /named
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/named /var/log/named
COPY --from=builder /var/cache/named /var/cache/named
USER 65534:65534
WORKDIR /app
EXPOSE 53 953
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/named", "-v"]
ENTRYPOINT ["/named"]
LABEL org.opencontainers.image.title="bind" \
      org.opencontainers.image.version="9.18.24" \
      org.opencontainers.image.vendor="ISC" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
