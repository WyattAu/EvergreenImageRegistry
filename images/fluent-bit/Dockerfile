# =============================================================================
# SOVEREIGN HARDENED FLUENT-BIT
# Generated from template - Version: 3.1.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/fluent/fluent-bit/releases/download/v3.1.0/fluent-bit-3.1.0-linux-amd64.tar.gz" -o /fluent-bit.tar.gz && \
    tar -xzf /fluent-bit.tar.gz -C / && rm /fluent-bit.tar.gz && chmod +x /fluent-bit 2>/dev/null || \
    curl -fsSL "https://github.com/fluent/fluent-bit/releases/download/v3.1.0/fluent-bit-3.1.0-linux-amd64.tar.gz" -o /fluent-bit && chmod +x /fluent-bit

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/fluent-bit /var/cache/fluent-bit

FROM scratch
COPY --from=downloader /fluent-bit /fluent-bit
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/fluent-bit /var/log/fluent-bit
COPY --from=builder /var/cache/fluent-bit /var/cache/fluent-bit
USER 65534:65534
WORKDIR /app
EXPOSE 2020
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/fluent-bit", "--version"]
ENTRYPOINT ["/fluent-bit"]
LABEL org.opencontainers.image.title="fluent-bit" \
      org.opencontainers.image.version="3.1.0" \
      org.opencontainers.image.vendor="Fluent" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
