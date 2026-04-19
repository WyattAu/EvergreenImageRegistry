# =============================================================================
# SOVEREIGN HARDENED DASHY
# Generated from template - Version: 2.1.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.1.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Lissy93/dashy/releases/download/v2.1.1/dashy-2.1.1-linux-x86_64.tar.gz" -o /dashy.tar.gz && \
    tar -xzf /dashy.tar.gz -C / && rm /dashy.tar.gz && chmod +x /dashy 2>/dev/null || \
    curl -fsSL "https://github.com/Lissy93/dashy/releases/download/v2.1.1/dashy-2.1.1-linux-x86_64.tar.gz" -o /dashy && chmod +x /dashy

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/dashy /var/cache/dashy

FROM scratch
COPY --from=downloader /dashy /dashy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/dashy /var/log/dashy
COPY --from=builder /var/cache/dashy /var/cache/dashy
USER 65534:65534
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/dashy", "--version"]
ENTRYPOINT ["/dashy"]
LABEL org.opencontainers.image.title="dashy" \
      org.opencontainers.image.version="2.1.1" \
      org.opencontainers.image.vendor="Dashy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
