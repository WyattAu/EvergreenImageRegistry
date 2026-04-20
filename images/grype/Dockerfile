# =============================================================================
# SOVEREIGN HARDENED GRYPE
# Generated from template - Version: 0.80.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.80.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/anchore/grype/releases/download/v0.80.0/grype_0.80.0_linux_amd64.tar.gz" -o /grype.tar.gz && \
    echo "a86a90074129cb72b47476f6ac3959eab95fba71f095521f5c8e58152463bd24  /grype.tar.gz" | sha256sum -c - && \
    tar -xzf /grype.tar.gz -C / && rm /grype.tar.gz && chmod +x /grype 2>/dev/null || \
    curl -fsSL "https://github.com/anchore/grype/releases/download/v0.80.0/grype_0.80.0_linux_amd64.tar.gz" -o /grype && chmod +x /grype

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/grype /var/cache/grype

FROM scratch
COPY --from=downloader /grype /grype
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/grype /var/log/grype
COPY --from=builder /var/cache/grype /var/cache/grype
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/grype", "version"]
ENTRYPOINT ["/grype"]
LABEL org.opencontainers.image.title="grype" \
      org.opencontainers.image.version="0.80.0" \
      org.opencontainers.image.vendor="Anchore" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
