# =============================================================================
# SOVEREIGN HARDENED DODB
# Constraint: debian-slim - niche database, placeholder binary
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: PLACEHOLDER - no upstream static binary available
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -s /sbin/nologin dodb 2>/dev/null || true
RUN mkdir -p /var/lib/dodb /var/log/dodb /var/cache/dodb /app
RUN printf '#!/bin/sh\necho "dodb v%s - placeholder (no upstream binary)"\nsleep infinity' "${VERSION}" > /app/dodb && chmod +x /app/dodb
RUN chown -R 65532:65532 /var/lib/dodb /var/log/dodb /var/cache/dodb /app
USER 65532:65532
WORKDIR /app
EXPOSE 6379
ENTRYPOINT ["/app/dodb"]
LABEL org.opencontainers.image.title="dodb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened DoDB - distributed object database (placeholder)" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="placeholder" \
      sovereign.image.note="No upstream binary available. Replace placeholder when upstream publishes releases." \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM