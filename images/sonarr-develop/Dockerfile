# =============================================================================
# SOVEREIGN HARDENED SONARR-DEVELOP
# Generated from template - Version: 4.0.11
# Constraint: debian-slim - .NET runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.0.11
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Sonarr/Sonarr/releases/download/v4.0.11/Sonarr.develop.4.0.11.linux-core-x64.tar.gz" -o /Sonarr.tar.gz && \
    tar -xzf /Sonarr.tar.gz -C /app && rm /Sonarr.tar.gz && chmod +x /app/Sonarr 2>/dev/null || \
    curl -fsSL "https://github.com/Sonarr/Sonarr/releases/download/v4.0.11/Sonarr.develop.4.0.11.linux-core-x64.tar.gz" -o /app/Sonarr && chmod +x /app/Sonarr

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
COPY --from=downloader --chown=65534:65534 /app /app
RUN mkdir -p /var/log/sonarr-develop /var/cache/sonarr-develop && chown -R 65534:65534 /var/log/sonarr-develop /var/cache/sonarr-develop 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 8989
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8989/api/v1/system/status || exit 1
ENTRYPOINT ["/app/Sonarr"]
LABEL org.opencontainers.image.title="sonarr-develop" \
      org.opencontainers.image.version="4.0.11" \
      org.opencontainers.image.vendor="Sonarr" \
      org.opencontainers.image.source="https://github.com/Sonarr/Sonarr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
