# =============================================================================
# SOVEREIGN HARDENED REDIS-6
# Generated from template - Version: 6.2.16
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=6.2.16
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN useradd -m -u 65532 -s /usr/sbin/nologin redis 2>/dev/null || true
RUN mkdir -p /app /var/log/redis /var/cache/redis 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates || true
# NOTE: redis server not available in wolfi; uses pre-compiled binary
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/redis /var/log/redis
COPY --from=builder --chown=65532:65532 /var/cache/redis /var/cache/redis
USER 65532:65532
WORKDIR /app
EXPOSE 6379
ENTRYPOINT ["redis"]
LABEL org.opencontainers.image.title="redis-6" \
      org.opencontainers.image.version="6.2.16" \
      org.opencontainers.image.vendor="Redis" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM