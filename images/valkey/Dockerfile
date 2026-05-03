# =============================================================================
# EVERGREEN HARDENED VALKEY
# Generated from template - Version: 7.2.4
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.2.4
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN useradd -m -u 65532 -s /usr/bin/false valkey 2>/dev/null || true
RUN mkdir -p /app /var/log/valkey /var/cache/valkey 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ENV HEALTH_CMD="valkey-cli ping" \
    READY_CMD="valkey-cli ping" \
    STARTUP_CMD="valkey-cli ping" \
    EVERGREEN_LOG_LEVEL=info

RUN apk add --no-cache valkey ca-certificates || true
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/valkey /var/log/valkey
COPY --from=builder --chown=65532:65532 /var/cache/valkey /var/cache/valkey
USER 65532:65532
WORKDIR /app
EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:6379/ || exit 1
ENTRYPOINT ["sh", "-c", "valkey"]
LABEL org.opencontainers.image.title="valkey" \
      org.opencontainers.image.version="7.2.4" \
      org.opencontainers.image.vendor="Valkey" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
