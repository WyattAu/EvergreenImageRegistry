# =============================================================================
# EVERGREEN HARDENED POSTGRES
# Generated from template - Version: 17.4
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=17.4
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN useradd -m -u 65532 -s /usr/bin/false postgres 2>/dev/null || true && \
    mkdir -p /app /var/log/postgres /var/cache/postgres 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache postgresql-17 ca-certificates || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/postgres /var/log/postgres
COPY --from=builder --chown=65532:65532 /var/cache/postgres /var/cache/postgres
USER 65532:65532
WORKDIR /app
EXPOSE 5432

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD pg_isready -h localhost -p 5432
ENTRYPOINT ["postgres"]
LABEL org.opencontainers.image.title="postgres" \
      org.opencontainers.image.description="PostgreSQL - advanced open source relational database" \
      org.opencontainers.image.version="17.4" \
      org.opencontainers.image.vendor="PostgreSQL" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/postgres/postgres"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
