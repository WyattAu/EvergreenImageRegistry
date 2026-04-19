# =============================================================================
# SOVEREIGN HARDENED STATPING
# Generated from template - Version: 0.90.75
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.90.75
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/statping/statping/releases/download/v0.90.75/statping-linux-amd64.tar.gz" -o /statping.tar.gz && \
    tar -xzf /statping.tar.gz -C / && rm /statping.tar.gz && chmod +x /statping 2>/dev/null || \
    curl -fsSL "https://github.com/statping/statping/releases/download/v0.90.75/statping-linux-amd64.tar.gz" -o /statping && chmod +x /statping

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/statping /var/cache/statping

FROM scratch
COPY --from=downloader /statping /statping
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/statping /var/log/statping
COPY --from=builder /var/cache/statping /var/cache/statping
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/statping", "--version"]
ENTRYPOINT ["/statping"]
LABEL org.opencontainers.image.title="statping" \
      org.opencontainers.image.version="0.90.75" \
      org.opencontainers.image.vendor="Statping" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
