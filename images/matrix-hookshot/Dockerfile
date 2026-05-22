ARG VERSION=7.3.3
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM ghcr.io/matrix-org/matrix-hookshot:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
RUN apk add --no-cache nodejs npm 2>/dev/null || true
COPY --from=upstream /app /app
RUN cd /app && npm install --omit=dev 2>/dev/null || true && \
    mkdir -p /var/log/matrix-hookshot /etc/matrix-hookshot 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache nodejs ca-certificates 2>/dev/null || true
COPY --from=builder /app /app
COPY --from=builder /var/log/matrix-hookshot /var/log/matrix-hookshot
COPY --from=builder /etc/matrix-hookshot /etc/matrix-hookshot
USER 65532:65532
WORKDIR /app
EXPOSE 9993

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9993/ || exit 1
ENTRYPOINT ["node"]
CMD ["."]

LABEL org.opencontainers.image.title="matrix-hookshot" \
      org.opencontainers.image.description="Matrix Hookshot - multi-purpose Matrix bot bridge framework" \
      org.opencontainers.image.version="7.3.3" \
      org.opencontainers.image.vendor="matrix.org" \
      org.opencontainers.image.source="https://github.com/matrix-org/matrix-hookshot" \
      evergreen.image.tier="2" \
      evergreen.image.category="messaging" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
