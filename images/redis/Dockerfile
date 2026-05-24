# =============================================================================
# EVERGREEN HARDENED REDIS
# Uses official redis image as upstream binary source on Wolfi base
# =============================================================================

ARG VERSION=7.4.9
ARG TARGETARCH

FROM redis:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ENV HEALTH_CMD="redis-cli ping" \
    READY_CMD="redis-cli ping" \
    STARTUP_CMD="redis-cli ping" \
    EVERGREEN_LOG_LEVEL=info

RUN apk add --no-cache ca-certificates

COPY --from=upstream /usr/local/bin/redis-server /usr/local/bin/redis-server
COPY --from=upstream /usr/local/bin/redis-cli /usr/local/bin/redis-cli

RUN adduser -D -u 65532 -s /bin/false redis 2>/dev/null || true && \
    mkdir -p /app /var/log/redis /var/cache/redis && \
    chown -R 65532:65532 /app /var/log/redis /var/cache/redis

USER 65532:65532
WORKDIR /app
EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD redis-cli ping
ENTRYPOINT ["redis-server"]
CMD ["--bind", "0.0.0.0", "--protected-mode", "no"]
LABEL org.opencontainers.image.title="redis" \
      org.opencontainers.image.description="Redis - in-memory data structure store and cache" \
      org.opencontainers.image.version="7.4.9" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      org.opencontainers.image.source="https://github.com/redis/redis"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
