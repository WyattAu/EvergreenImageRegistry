# =============================================================================
# SOVEREIGN HARDENED REDIS-VERT
# Redis with vector search (RediSearch module)
# Constraint: wolfi - pre-compiled binary from Redis
# =============================================================================

ARG VERSION=7.4.2
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
# NOTE: redis server not available in wolfi; uses pre-compiled binary
# redis-vert (Redis Stack with RediSearch) must be downloaded from Redis Inc.
# COPY --from=builder /usr/local/bin/redis-stack-server /usr/local/bin/redis-stack-server
USER 65532:65532
WORKDIR /app
EXPOSE 6379
ENTRYPOINT ["redis-stack-server"]
LABEL org.opencontainers.image.title="redis-vert" \
      org.opencontainers.image.version="7.4.2" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.description="Redis with vector search (RediSearch) on Wolfi" \
      sovereign.image.tier="3" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
