# =============================================================================
# SOVEREIGN HARDENED OUTLINE
# Generated from template - Version: 0.77.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.77.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache nodejs npm postgresql-client ca-certificates
RUN adduser -u 65532 -G '' -D outline 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R outline:outline /app /var/log/node /var/cache/node 2>/dev/null || true
USER outline
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="outline" \
      org.opencontainers.image.version="0.77.0" \
      org.opencontainers.image.vendor="Outline" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM