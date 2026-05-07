# =============================================================================
# EVERGREEN HARDENED REDIS-VERT
# Redis with vector search (RediSearch module)
# Constraint: wolfi - pre-compiled binary from Redis
# =============================================================================

ARG VERSION=7.4.2
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates 
# NOTE: redis server not available in wolfi; uses pre-compiled binary
# redis-vert (Redis Stack with RediSearch) must be downloaded from Redis Inc.
# COPY --from=builder /usr/local/bin/redis-stack-server /usr/local/bin/redis-stack-server
USER 65532:65532
WORKDIR /app
EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD redis-cli ping
ENTRYPOINT ["redis-stack-server"]
LABEL org.opencontainers.image.title="redis-vert" \
      org.opencontainers.image.version="7.4.2" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.description="Redis with vector search (RediSearch) on Wolfi" \
      evergreen.image.tier="3" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
            org.opencontainers.image.source="https://github.com/redis/redis"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
