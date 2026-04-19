# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL-15
# Generated from template - Version: 15.7
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=15.7
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65534 -s /usr/sbin/nologin postgres 2>/dev/null || true
RUN mkdir -p /app /var/log/postgres /var/cache/postgres

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-15 ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get purge -y --auto-remove apt apt-get dpkg 2>/dev/null || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/postgres /var/log/postgres
COPY --from=builder --chown=65534:65534 /var/cache/postgres /var/cache/postgres
USER 65534:65534
WORKDIR /app
EXPOSE 5432
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD pg_isready -h localhost
ENTRYPOINT ["postgres"]
LABEL org.opencontainers.image.title="postgresql-15" \
      org.opencontainers.image.version="15.7" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.constraint.hardened="true"
