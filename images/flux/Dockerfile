# =============================================================================
# SOVEREIGN HARDENED FLUX
# Generated from template - Version: 2.3.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=2.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends flux ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' flux 2>/dev/null || true
RUN mkdir -p /app /var/log/flux /var/cache/flux && chown -R flux:flux /app /var/log/flux /var/cache/flux 2>/dev/null || true
USER flux:flux
WORKDIR /app
EXPOSE 3030
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /./
ENTRYPOINT ["flux"]
LABEL org.opencontainers.image.title="flux" \
      org.opencontainers.image.version="2.3.0" \
      org.opencontainers.image.vendor="Flux" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
