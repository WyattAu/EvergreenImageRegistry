# =============================================================================
# SOVEREIGN HARDENED CORTEX
# Generated from template - Version: 1.15.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.15.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/cortexproject/cortex/releases/download/v1.15.1/cortex-linux-amd64" -o /cortex.tar.gz && \
    tar -xzf /cortex.tar.gz -C / && rm /cortex.tar.gz && chmod +x /cortex 2>/dev/null || \
    curl -fsSL "https://github.com/cortexproject/cortex/releases/download/v1.15.1/cortex-linux-amd64" -o /cortex && chmod +x /cortex

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cortex /var/cache/cortex

FROM scratch
COPY --from=downloader /cortex /cortex
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cortex /var/log/cortex
COPY --from=builder /var/cache/cortex /var/cache/cortex
USER 65534:65534
WORKDIR /app
EXPOSE 9009
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/cortex", "--version"]
ENTRYPOINT ["/cortex"]
LABEL org.opencontainers.image.title="cortex" \
      org.opencontainers.image.version="1.15.1" \
      org.opencontainers.image.vendor="Cortex" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
