# =============================================================================
# SOVEREIGN HARDENED IT-TOOLS
# Generated from template - Version: 2024.4.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2024.4.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/CorentinTh/it-tools/releases/download/v2024.4.1/it-tools-2024.4.1-linux-amd64.tar.gz" -o /it-tools.tar.gz && \
    tar -xzf /it-tools.tar.gz -C / && rm /it-tools.tar.gz && chmod +x /it-tools 2>/dev/null || \
    curl -fsSL "https://github.com/CorentinTh/it-tools/releases/download/v2024.4.1/it-tools-2024.4.1-linux-amd64.tar.gz" -o /it-tools && chmod +x /it-tools

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/it-tools /var/cache/it-tools

FROM scratch
COPY --from=downloader /it-tools /it-tools
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/it-tools /var/log/it-tools
COPY --from=builder /var/cache/it-tools /var/cache/it-tools
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/it-tools", "--version"]
ENTRYPOINT ["/it-tools"]
LABEL org.opencontainers.image.title="it-tools" \
      org.opencontainers.image.version="2024.4.1" \
      org.opencontainers.image.vendor="IT-Tools" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
