# =============================================================================
# SOVEREIGN HARDENED RADARR-DEVELOP
# Generated from template - Version: 5.15.0
# Constraint: debian-slim - .NET runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.15.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Radarr/Radarr/releases/download/v5.15.0/Radarr.develop.5.15.0.linux-core-x64.tar.gz" -o /Radarr.tar.gz && \
    tar -xzf /Radarr.tar.gz -C /app && rm /Radarr.tar.gz && chmod +x /app/Radarr 2>/dev/null || \
    curl -fsSL "https://github.com/Radarr/Radarr/releases/download/v5.15.0/Radarr.develop.5.15.0.linux-core-x64.tar.gz" -o /app/Radarr && chmod +x /app/Radarr

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
COPY --from=downloader --chown=65534:65534 /app /app
RUN mkdir -p /var/log/radarr-develop /var/cache/radarr-develop && chown -R 65534:65534 /var/log/radarr-develop /var/cache/radarr-develop 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 7878
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:7878/api/v1/system/status || exit 1
ENTRYPOINT ["/app/Radarr"]
LABEL org.opencontainers.image.title="radarr-develop" \
      org.opencontainers.image.version="5.15.0" \
      org.opencontainers.image.vendor="Radarr" \
      org.opencontainers.image.source="https://github.com/Radarr/Radarr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
