# =============================================================================
# SOVEREIGN HARDENED DNSDIST
# Generated from template - Version: 1.9.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.9.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dnsdist.org/dnsdist-1.9.0.tar.gz" -o /dnsdist.tar.gz && \
    tar -xzf /dnsdist.tar.gz -C / && rm /dnsdist.tar.gz && chmod +x /dnsdist 2>/dev/null || \
    curl -fsSL "https://dnsdist.org/dnsdist-1.9.0.tar.gz" -o /dnsdist && chmod +x /dnsdist

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/dnsdist /var/cache/dnsdist

FROM scratch
COPY --from=downloader /dnsdist /dnsdist
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/dnsdist /var/log/dnsdist
COPY --from=builder /var/cache/dnsdist /var/cache/dnsdist
USER 65534:65534
WORKDIR /app
EXPOSE 53 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD dnsdist dnsdist --version
ENTRYPOINT ["/dnsdist"]
LABEL org.opencontainers.image.title="dnsdist" \
      org.opencontainers.image.version="1.9.0" \
      org.opencontainers.image.vendor="PowerDNS" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
