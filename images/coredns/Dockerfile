# =============================================================================
# SOVEREIGN HARDENED COREDNS
# Generated from template - Version: 1.12.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.12.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/coredns/coredns/releases/download/v1.12.0/coredns_1.12.0_linux_amd64.tgz" -o /coredns.tar.gz && \
    tar -xzf /coredns.tar.gz -C / && rm /coredns.tar.gz && chmod +x /coredns 2>/dev/null || \
    curl -fsSL "https://github.com/coredns/coredns/releases/download/v1.12.0/coredns_1.12.0_linux_amd64.tgz" -o /coredns && chmod +x /coredns

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/coredns /var/cache/coredns

FROM scratch
COPY --from=downloader /coredns /coredns
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/coredns /var/log/coredns
COPY --from=builder /var/cache/coredns /var/cache/coredns
USER 65534:65534
WORKDIR /app
EXPOSE 53
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD coredns coredns --version
ENTRYPOINT ["/coredns"]
LABEL org.opencontainers.image.title="coredns" \
      org.opencontainers.image.version="1.12.0" \
      org.opencontainers.image.vendor="Coredns" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
