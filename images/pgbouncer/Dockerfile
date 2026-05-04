# =============================================================================
# EVERGREEN HARDENED PGBOUNCER
# Generated from template - Version: 1.22.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.22.1
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D pgbouncer 2>/dev/null || true && \
    mkdir -p /app /var/log/pgbouncer /var/cache/pgbouncer && chown -R pgbouncer:pgbouncer /app /var/log/pgbouncer /var/cache/pgbouncer 2>/dev/null || true
USER pgbouncer
WORKDIR /app
EXPOSE 6432

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:6432/ || exit 1
ENTRYPOINT ["pgbouncer"]
LABEL org.opencontainers.image.title="pgbouncer" \
      org.opencontainers.image.description="pgbouncer container image" \
      org.opencontainers.image.version="1.22.1" \
      org.opencontainers.image.vendor="PgBouncer" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
