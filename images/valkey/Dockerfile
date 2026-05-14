ARG VERSION=9
ARG BUILD_DATE

ARG TARGETARCH

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ENV HEALTH_CMD="valkey-cli ping" \
    READY_CMD="valkey-cli ping" \
    STARTUP_CMD="valkey-cli ping" \
    EVERGREEN_LOG_LEVEL=info

RUN apk add --no-cache valkey ca-certificates || true
RUN mkdir -p /app /var/log/valkey /var/cache/valkey 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD valkey-cli ping || exit 1
ENTRYPOINT ["sh", "-c", "valkey"]
LABEL org.opencontainers.image.title="valkey" \
      org.opencontainers.image.description="Valkey - open source Redis-compatible in-memory data store" \
      org.opencontainers.image.version="9" \
      org.opencontainers.image.vendor="Valkey" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
            org.opencontainers.image.source="https://github.com/valkey-io/valkey"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
