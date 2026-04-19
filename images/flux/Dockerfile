# =============================================================================
# SOVEREIGN HARDENED FLUX
# Generated from template - Version: 2.3.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/fluxcd/flux2/releases/download/v2.3.0/flux_2.3.0_linux_amd64.tar.gz" -o /flux.tar.gz && \
    tar -xzf /flux.tar.gz -C / && rm /flux.tar.gz && chmod +x /flux 2>/dev/null || \
    curl -fsSL "https://github.com/fluxcd/flux2/releases/download/v2.3.0/flux_2.3.0_linux_amd64.tar.gz" -o /flux && chmod +x /flux

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/flux /var/cache/flux

FROM scratch
COPY --from=downloader /flux /flux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/flux /var/log/flux
COPY --from=builder /var/cache/flux /var/cache/flux
USER 65534:65534
WORKDIR /app
EXPOSE 3030
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD flux flux --version
ENTRYPOINT ["/flux"]
LABEL org.opencontainers.image.title="flux" \
      org.opencontainers.image.version="2.3.0" \
      org.opencontainers.image.vendor="Flux" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
