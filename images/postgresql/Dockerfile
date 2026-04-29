# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL
# Generated from template - Version: 17.4
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=17.4
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65532 -s /usr/bin/false postgres 2>/dev/null || true
RUN mkdir -p /app /var/log/postgres /var/cache/postgres 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ENV HEALTH_CMD="pg_isready -h localhost" \READY_
CMD="pg_isready -h localhost -q" \STARTUP_
CMD="pg_isready -h localhost" \
    SOVEREIGN_LOG_LEVEL=info

RUN apk add --no-cache postgresql-17 ca-certificates || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/postgres /var/log/postgres
COPY --from=builder --chown=65532:65532 /var/cache/postgres /var/cache/postgres
USER 65532:65532
WORKDIR /app
EXPOSE 5432
ENTRYPOINT ["sh", "-c", "postgres"]
LABEL org.opencontainers.image.title="postgresql" \
      org.opencontainers.image.version="17.4" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM