# =============================================================================
# SOVEREIGN HARDENED MEMCACHED
# Generated from template - Version: 1.6.26
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.6.26
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65532 -s /usr/sbin/nologin memcached 2>/dev/null || true
RUN mkdir -p /app /var/log/memcached /var/cache/memcached 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache memcached ca-certificates 
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/memcached /var/log/memcached
COPY --from=builder --chown=65532:65532 /var/cache/memcached /var/cache/memcached
USER 65532:65532
WORKDIR /app
EXPOSE 11211
ENTRYPOINT ["memcached"]
LABEL org.opencontainers.image.title="memcached" \
      org.opencontainers.image.version="1.6.26" \
      org.opencontainers.image.vendor="Memcached" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM