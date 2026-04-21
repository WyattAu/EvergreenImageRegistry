# =============================================================================
# SOVEREIGN HARDENED VULCAN
# Constraint: debian-slim - niche tool, placeholder binary
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: PLACEHOLDER - no upstream static binary available
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin vulcan 2>/dev/null || true
RUN mkdir -p /var/lib/vulcan /var/log/vulcan /var/cache/vulcan /app
RUN printf '#!/bin/sh\necho "vulcan v%s - placeholder (no upstream binary)"\nsleep infinity' "${VERSION}" > /app/vulcan && chmod +x /app/vulcan
RUN chown -R 65534:65534 /var/lib/vulcan /var/log/vulcan /var/cache/vulcan /app
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/app/vulcan"]
ENTRYPOINT ["/app/vulcan"]
LABEL org.opencontainers.image.title="vulcan" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Vulcan - niche tool (placeholder)" \
      sovereign.image.tier="1" \
      sovereign.image.category="tooling" \
      sovereign.image.status="placeholder" \
      sovereign.image.note="No upstream binary available. Replace placeholder when upstream publishes releases." \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
