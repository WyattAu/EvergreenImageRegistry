# =============================================================================
# SOVEREIGN HARDENED READARR
# Generated from template - Version: 0.4.5
# Constraint: debian-slim - .NET runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.4.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Readarr/Readarr/releases/download/v0.4.5/Readarr.develop.0.4.5.linux-core-x64.tar.gz" -o /Readarr.tar.gz && \
    tar -xzf /Readarr.tar.gz -C /app && rm /Readarr.tar.gz && chmod +x /app/Readarr 2>/dev/null || \
    curl -fsSL "https://github.com/Readarr/Readarr/releases/download/v0.4.5/Readarr.develop.0.4.5.linux-core-x64.tar.gz" -o /app/Readarr && chmod +x /app/Readarr

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
COPY --from=downloader --chown=65534:65534 /app /app
RUN mkdir -p /var/log/readarr /var/cache/readarr && chown -R 65534:65534 /var/log/readarr /var/cache/readarr 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 8787
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8787/api/v1/system/status || exit 1
ENTRYPOINT ["/app/Readarr"]
LABEL org.opencontainers.image.title="readarr" \
      org.opencontainers.image.version="0.4.5" \
      org.opencontainers.image.vendor="Readarr" \
      org.opencontainers.image.source="https://github.com/Readarr/Readarr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
