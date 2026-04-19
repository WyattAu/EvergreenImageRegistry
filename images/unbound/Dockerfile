# =============================================================================
# SOVEREIGN HARDENED UNBOUND
# Generated from template - Version: 1.20.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.20.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://unbound.net/downloads/unbound-1.20.0.tar.gz" -o /unbound.tar.gz && \
    tar -xzf /unbound.tar.gz -C / && rm /unbound.tar.gz && chmod +x /unbound 2>/dev/null || \
    curl -fsSL "https://unbound.net/downloads/unbound-1.20.0.tar.gz" -o /unbound && chmod +x /unbound

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/unbound /var/cache/unbound

FROM scratch
COPY --from=downloader /unbound /unbound
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/unbound /var/log/unbound
COPY --from=builder /var/cache/unbound /var/cache/unbound
USER 65534:65534
WORKDIR /app
EXPOSE 53
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/unbound", "-h"]
ENTRYPOINT ["/unbound"]
LABEL org.opencontainers.image.title="unbound" \
      org.opencontainers.image.version="1.20.0" \
      org.opencontainers.image.vendor="NLnet Labs" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
