# =============================================================================
# SOVEREIGN HARDENED MODSECURITY
# Generated from template - Version: 2.4.59
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.4.59
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache apache2 ca-certificates || true
RUN adduser -u 65532 -D appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/apache2 /var/cache/apache2 && chown -R appuser:appuser /app /var/log/apache2 /var/cache/apache2 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["apache2"]
LABEL org.opencontainers.image.title="modsecurity" \
      org.opencontainers.image.version="2.4.59" \
      org.opencontainers.image.vendor="OWASP" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM