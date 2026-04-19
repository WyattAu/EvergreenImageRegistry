# =============================================================================
# SOVEREIGN HARDENED ENVOY
# Generated from template - Version: 1.31.0
# Constraint: distroless - minimal runtime, no shell, CVE-free
# Priority: scratch > distroless (2nd best) > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.31.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://envoy.io/" -o /envoy.tar.gz && \
    tar -xzf /envoy.tar.gz -C / && rm /envoy.tar.gz && chmod +x /envoy

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/envoy /var/cache/envoy

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /envoy /envoy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/envoy /var/log/envoy
COPY --from=builder /var/cache/envoy /var/cache/envoy
USER 65534:65534
WORKDIR /app
EXPOSE 80 443 9900
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD envoy --version 2>/dev/null || exit 1
ENTRYPOINT ["/envoy"]
LABEL org.opencontainers.image.title="envoy" \
      org.opencontainers.image.version="1.31.0" \
      org.opencontainers.image.vendor="Envoy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
