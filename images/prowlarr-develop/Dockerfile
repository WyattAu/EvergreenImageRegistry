# =============================================================================
# SOVEREIGN HARDENED PROWLARR-DEVELOP
# Generated from template - Version: 1.29.0
# Constraint: debian-slim - .NET runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.29.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Prowlarr/Prowlarr/releases/download/v1.29.0/Prowlarr.develop.1.29.0.linux-core-x64.tar.gz" -o /Prowlarr.tar.gz && \
    tar -xzf /Prowlarr.tar.gz -C /app && rm /Prowlarr.tar.gz && chmod +x /app/Prowlarr 2>/dev/null || \
    curl -fsSL "https://github.com/Prowlarr/Prowlarr/releases/download/v1.29.0/Prowlarr.develop.1.29.0.linux-core-x64.tar.gz" -o /app/Prowlarr && chmod +x /app/Prowlarr

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
COPY --from=downloader --chown=65534:65534 /app /app
RUN mkdir -p /var/log/prowlarr-develop /var/cache/prowlarr-develop && chown -R 65534:65534 /var/log/prowlarr-develop /var/cache/prowlarr-develop 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 9696
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:9696/api/v1/system/status || exit 1
ENTRYPOINT ["/app/Prowlarr"]
LABEL org.opencontainers.image.title="prowlarr-develop" \
      org.opencontainers.image.version="1.29.0" \
      org.opencontainers.image.vendor="Prowlarr" \
      org.opencontainers.image.source="https://github.com/Prowlarr/Prowlarr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
