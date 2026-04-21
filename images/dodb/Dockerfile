# =============================================================================
# SOVEREIGN HARDENED DODB
# Constraint: debian-slim - niche database, placeholder binary
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: PLACEHOLDER - no upstream static binary available
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin dodb 2>/dev/null || true
RUN mkdir -p /var/lib/dodb /var/log/dodb /var/cache/dodb /app
RUN printf '#!/bin/sh\necho "dodb v%s - placeholder (no upstream binary)"\nsleep infinity' "${VERSION}" > /app/dodb && chmod +x /app/dodb
RUN chown -R 65534:65534 /var/lib/dodb /var/log/dodb /var/cache/dodb /app
USER 65534:65534
WORKDIR /app
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/app/dodb"]
ENTRYPOINT ["/app/dodb"]
LABEL org.opencontainers.image.title="dodb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened DoDB - distributed object database (placeholder)" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="placeholder" \
      sovereign.image.note="No upstream binary available. Replace placeholder when upstream publishes releases." \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
