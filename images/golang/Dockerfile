# =============================================================================
# SOVEREIGN HARDENED GOLANG
# Generated from template - Version: 1.22.3
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.22.3
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends golang-go ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' go 2>/dev/null || true
RUN mkdir -p /app /var/log/go /var/cache/go && chown -R go:go /app /var/log/go /var/cache/go 2>/dev/null || true
USER go
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD go go version
ENTRYPOINT ["go"]
LABEL org.opencontainers.image.title="golang" \
      org.opencontainers.image.version="1.22.3" \
      org.opencontainers.image.vendor="Go" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
