# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL-16
# Generated from template - Version: 16.3
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=16.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65532 -s /usr/sbin/nologin postgres 2>/dev/null || true
RUN mkdir -p /app /var/log/postgres /var/cache/postgres

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache postgresql-16 ca-certificates
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/postgres /var/log/postgres
COPY --from=builder --chown=65532:65532 /var/cache/postgres /var/cache/postgres
USER 65532:65532
WORKDIR /app
EXPOSE 5432
ENTRYPOINT ["postgres"]
LABEL org.opencontainers.image.title="postgresql-16" \
      org.opencontainers.image.version="16.3" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM