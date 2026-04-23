# =============================================================================
# SOVEREIGN HARDENED PGPOOL-II
# Generated from template - Version: 4.5.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.5.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -G '' -D pgpool 2>/dev/null || true
RUN mkdir -p /app /var/log/pgpool /var/cache/pgpool && chown -R pgpool:pgpool /app /var/log/pgpool /var/cache/pgpool 2>/dev/null || true
USER pgpool
WORKDIR /app
EXPOSE 9999
ENTRYPOINT ["pgpool"]
LABEL org.opencontainers.image.title="pgpool-II" \
      org.opencontainers.image.version="4.5.1" \
      org.opencontainers.image.vendor="PgPool" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM