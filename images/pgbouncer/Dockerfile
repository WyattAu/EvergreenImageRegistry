# =============================================================================
# EVERGREEN HARDENED PGBOUNCER
# Generated from template - Version: 1.22.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.22.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D pgbouncer 2>/dev/null || true && \
    mkdir -p /app /var/log/pgbouncer /var/cache/pgbouncer && chown -R pgbouncer:pgbouncer /app /var/log/pgbouncer /var/cache/pgbouncer 2>/dev/null || true
USER pgbouncer
WORKDIR /app
EXPOSE 6432

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:6432/ || exit 1
ENTRYPOINT ["pgbouncer"]
LABEL org.opencontainers.image.title="pgbouncer" \
      org.opencontainers.image.description="pgbouncer container image" \
      org.opencontainers.image.version="1.22.1" \
      org.opencontainers.image.vendor="PgBouncer" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/pgbouncer/pgbouncer"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
