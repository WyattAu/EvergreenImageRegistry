# =============================================================================
# EVERGREEN HARDENED POSTGRESQL
# Generated from template - Version: 17.4
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=17.4
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN useradd -m -u 65532 -s /usr/bin/false postgres 2>/dev/null || true && \
    mkdir -p /app /var/log/postgres /var/cache/postgres 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ENV HEALTH_CMD="pg_isready -h localhost" \
    READY_CMD="pg_isready -h localhost -q" \
    STARTUP_CMD="pg_isready -h localhost" \
    EVERGREEN_LOG_LEVEL=info

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
ENTRYPOINT ["sh", "-c", "postgres"]
LABEL org.opencontainers.image.title="postgresql" \
      org.opencontainers.image.description="PostgreSQL - advanced open source relational database" \
      org.opencontainers.image.version="17.4" \
      org.opencontainers.image.vendor="PostgreSQL" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
            org.opencontainers.image.source="https://github.com/postgres/postgres"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
