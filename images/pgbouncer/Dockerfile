# =============================================================================
# SOVEREIGN HARDENED PGBOUNCER
# Generated from template - Version: 1.22.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.22.1
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -G '' -D pgbouncer 2>/dev/null || true
RUN mkdir -p /app /var/log/pgbouncer /var/cache/pgbouncer && chown -R pgbouncer:pgbouncer /app /var/log/pgbouncer /var/cache/pgbouncer 2>/dev/null || true
USER pgbouncer
WORKDIR /app
EXPOSE 6432
ENTRYPOINT ["pgbouncer"]
LABEL org.opencontainers.image.title="pgbouncer" \
      org.opencontainers.image.version="1.22.1" \
      org.opencontainers.image.vendor="PgBouncer" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM