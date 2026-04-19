# =============================================================================
# SOVEREIGN HARDENED NETMAKER
# Generated from template - Version: 0.24.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.24.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/gravitl/netmaker/releases/download/v0.24.0/netmaker-0.24.0-linux-amd64.tar.gz" -o /netmaker.tar.gz && \
    tar -xzf /netmaker.tar.gz -C / && rm /netmaker.tar.gz && chmod +x /netmaker 2>/dev/null || \
    curl -fsSL "https://github.com/gravitl/netmaker/releases/download/v0.24.0/netmaker-0.24.0-linux-amd64.tar.gz" -o /netmaker && chmod +x /netmaker

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/netmaker /var/cache/netmaker

FROM scratch
COPY --from=downloader /netmaker /netmaker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/netmaker /var/log/netmaker
COPY --from=builder /var/cache/netmaker /var/cache/netmaker
USER 65534:65534
WORKDIR /app
EXPOSE 443 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/netmaker", "--version"]
ENTRYPOINT ["/netmaker"]
LABEL org.opencontainers.image.title="netmaker" \
      org.opencontainers.image.version="0.24.0" \
      org.opencontainers.image.vendor="NetMaker" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
