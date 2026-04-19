# =============================================================================
# SOVEREIGN HARDENED DNSMASQ
# Generated from template - Version: 2.90
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.90
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "http://www.thekelleys.org.uk/dnsmasq/dnsmasq-2.90.tar.gz" -o /dnsmasq.tar.gz && \
    tar -xzf /dnsmasq.tar.gz -C / && rm /dnsmasq.tar.gz && chmod +x /dnsmasq 2>/dev/null || \
    curl -fsSL "http://www.thekelleys.org.uk/dnsmasq/dnsmasq-2.90.tar.gz" -o /dnsmasq && chmod +x /dnsmasq

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/dnsmasq /var/cache/dnsmasq

FROM scratch
COPY --from=downloader /dnsmasq /dnsmasq
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/dnsmasq /var/log/dnsmasq
COPY --from=builder /var/cache/dnsmasq /var/cache/dnsmasq
USER 65534:65534
WORKDIR /app
EXPOSE 53
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/dnsmasq", "--version"]
ENTRYPOINT ["/dnsmasq"]
LABEL org.opencontainers.image.title="dnsmasq" \
      org.opencontainers.image.version="2.90" \
      org.opencontainers.image.vendor="Dnsmasq" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
