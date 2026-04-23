# =============================================================================
# SOVEREIGN HARDENED POWERDNS
# Generated from template - Version: 4.9.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.9.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -G '' -D appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/pdns /var/cache/pdns && chown -R appuser:appuser /app /var/log/pdns /var/cache/pdns 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 53 8081
ENTRYPOINT ["pdns"]
LABEL org.opencontainers.image.title="powerdns" \
      org.opencontainers.image.version="4.9.1" \
      org.opencontainers.image.vendor="PowerDNS" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM