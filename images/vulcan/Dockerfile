# =============================================================================
# SOVEREIGN HARDENED VULCAN
# Constraint: debian-slim - niche tool, placeholder binary
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: PLACEHOLDER - no upstream static binary available
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
ARG VERSION
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -s /usr/sbin/nologin vulcan 2>/dev/null || true
RUN mkdir -p /var/lib/vulcan /var/log/vulcan /var/cache/vulcan /app
RUN printf '#!/bin/sh\necho "vulcan v%s - placeholder (no upstream binary)"\nsleep infinity' "${VERSION}" > /app/vulcan && chmod +x /app/vulcan
RUN chown -R 65532:65532 /var/lib/vulcan /var/log/vulcan /var/cache/vulcan /app
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/app/vulcan"]
LABEL org.opencontainers.image.title="vulcan" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Vulcan - niche tool (placeholder)" \
      sovereign.image.tier="1" \
      sovereign.image.category="tooling" \
      sovereign.image.status="placeholder" \
      sovereign.image.note="No upstream binary available. Replace placeholder when upstream publishes releases." \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM