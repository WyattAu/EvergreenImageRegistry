# =============================================================================
# SOVEREIGN HARDENED HOMEASSISTANT
# Generated from template - Version: 2024.4.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2024.4.2
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3 py3-pip ca-certificates
RUN adduser -u 65532 -G '' -D homeassistant 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R homeassistant:homeassistant /app /var/log/python /var/cache/python 2>/dev/null || true
USER homeassistant
WORKDIR /app
EXPOSE 8123
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="homeassistant" \
      org.opencontainers.image.version="2024.4.2" \
      org.opencontainers.image.vendor="Home Assistant" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM