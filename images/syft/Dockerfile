# =============================================================================
# SOVEREIGN HARDENED SYFT
# Generated from template - Version: 1.8.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/anchore/syft/releases/download/v1.8.0/syft_1.8.0_linux_amd64.tar.gz" -o /syft.tar.gz && \
    tar -xzf /syft.tar.gz -C / && rm /syft.tar.gz && chmod +x /syft

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/syft /var/cache/syft

FROM scratch
COPY --from=downloader /syft /syft
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/syft /var/log/syft
COPY --from=builder /var/cache/syft /var/cache/syft
USER 65534:65534
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD syft version 2>/dev/null || exit 1
ENTRYPOINT ["/syft"]
LABEL org.opencontainers.image.title="syft" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Anchore" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
