# =============================================================================
# SOVEREIGN HARDENED WHISPARR
# Generated from template - Version: 1.0.0.329
# Constraint: debian-slim - .NET runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.0.0.329
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/Whisparr/Whisparr/releases/download/v1.0.0.329/Whisparr.develop.1.0.0.329.linux-core-x64.tar.gz" -o /Whisparr.tar.gz && \
    tar -xzf /Whisparr.tar.gz -C /app && rm /Whisparr.tar.gz && chmod +x /app/Whisparr 2>/dev/null || \
    curl -fsSL "https://github.com/Whisparr/Whisparr/releases/download/v1.0.0.329/Whisparr.develop.1.0.0.329.linux-core-x64.tar.gz" -o /app/Whisparr && chmod +x /app/Whisparr

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' app 2>/dev/null || true
COPY --from=downloader --chown=65534:65534 /app /app
RUN mkdir -p /var/log/whisparr /var/cache/whisparr && chown -R 65534:65534 /var/log/whisparr /var/cache/whisparr 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 6969
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:6969/api/v1/system/status || exit 1
ENTRYPOINT ["/app/Whisparr"]
LABEL org.opencontainers.image.title="whisparr" \
      org.opencontainers.image.version="1.0.0.329" \
      org.opencontainers.image.vendor="Whisparr" \
      org.opencontainers.image.source="https://github.com/Whisparr/Whisparr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
