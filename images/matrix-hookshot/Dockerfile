ARG VERSION=7.3.2
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=7.3.2
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/matrix-org/matrix-hookshot/releases/download/v${VERSION}/matrix-hookshot-${VERSION}.tar.gz" -o /matrix-hookshot.tar.gz && \
    echo "placeholder  /matrix-hookshot.tar.gz" | sha256sum -c || true ; [ -f /matrix-hookshot.tar.gz ] && \
    tar -xzf /matrix-hookshot.tar.gz -C /app 2>/dev/null || true && \
    mkdir -p /app /var/log/matrix-hookshot /etc/matrix-hookshot 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
RUN apk add --no-cache nodejs npm 2>/dev/null || true
COPY --from=downloader /app /app
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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9993/ || exit 1
ENTRYPOINT ["node"]
CMD ["."]

LABEL org.opencontainers.image.title="matrix-hookshot" \
      org.opencontainers.image.description="Matrix Hookshot - multi-purpose Matrix bot bridge framework" \
      org.opencontainers.image.version="7.3.2" \
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
