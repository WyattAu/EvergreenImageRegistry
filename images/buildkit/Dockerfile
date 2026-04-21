# =============================================================================
# SOVEREIGN HARDENED BUILDKIT
# Generated from template - Version: 0.29.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.29.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/moby/buildkit/releases/download/v${VERSION}/buildkit-v${VERSION}.linux-amd64.tar.gz" -o /tmp/buildkit.tar.gz && \
    tar -xzf /tmp/buildkit.tar.gz -C /usr/local && rm /tmp/buildkit.tar.gz && \
    chmod +x /usr/local/bin/buildkitd
RUN useradd -m -u 65534 -g '' buildkit 2>/dev/null || true
RUN mkdir -p /app /var/log/buildkitd /var/cache/buildkitd && chown -R buildkit:buildkit /app /var/log/buildkitd /var/cache/buildkitd 2>/dev/null || true
USER buildkit
WORKDIR /app
EXPOSE 1234
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:1234/debug/info
ENTRYPOINT ["buildkitd"]
LABEL org.opencontainers.image.title="buildkit" \
      org.opencontainers.image.version="0.29.0" \
      org.opencontainers.image.vendor="BuildKit" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
