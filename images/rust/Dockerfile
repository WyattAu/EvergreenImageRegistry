# =============================================================================
# SOVEREIGN HARDENED RUST
# Generated from template - Version: 1.78.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.78.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends rustc cargo ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' rust 2>/dev/null || true
RUN mkdir -p /app /var/log/rustc /var/cache/rustc && chown -R rust:rust /app /var/log/rustc /var/cache/rustc 2>/dev/null || true
USER rust
WORKDIR /app
EXPOSE 
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD rustc rustc --version
ENTRYPOINT ["rustc"]
LABEL org.opencontainers.image.title="rust" \
      org.opencontainers.image.version="1.78.0" \
      org.opencontainers.image.vendor="Rust" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
