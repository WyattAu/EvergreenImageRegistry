# =============================================================================
# SOVEREIGN HARDENED LOCALAI
# Generated from template - Version: 2.0.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mudler/LocalAI/releases/download/v2.0.0/localai-2.0.0-linux-amd64.tar.gz" -o /localai.tar.gz && \
    tar -xzf /localai.tar.gz -C / && rm /localai.tar.gz && chmod +x /localai 2>/dev/null || \
    curl -fsSL "https://github.com/mudler/LocalAI/releases/download/v2.0.0/localai-2.0.0-linux-amd64.tar.gz" -o /localai && chmod +x /localai

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/localai /var/cache/localai

FROM scratch
COPY --from=downloader /localai /localai
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/localai /var/log/localai
COPY --from=builder /var/cache/localai /var/cache/localai
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/localai", "--version"]
ENTRYPOINT ["/localai"]
LABEL org.opencontainers.image.title="localai" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.vendor="LocalAI" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
