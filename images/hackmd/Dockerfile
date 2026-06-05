ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=2.6.0
ARG TARGETARCH
RUN apk add --no-cache nodejs-20 npm ca-certificates git python3 make gcc && \
    mkdir -p /app-src 2>/dev/null || true
WORKDIR /tmp
RUN curl --retry 3 -fsSL \
    "https://github.com/hackmdio/hackmd-ce/releases/download/v${VERSION}/hackmd-ce-v${VERSION}.tar.gz" \
    -o /app.tar.gz && \
    tar -xzf /app.tar.gz -C /app-src --strip-components=1 && \
    rm -f /app.tar.gz && \
    cd /app-src && \
    npm install --omit=dev --legacy-peer-deps 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true && \
    mkdir -p /app/data /app/uploads 2>/dev/null || true && \
    chown -R 65532:65532 /app-src /app/data /app/uploads 2>/dev/null || true
USER 65532:65532
WORKDIR /app-src
EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="hackmd" \
      org.opencontainers.image.description="HackMD CE - collaborative markdown notes" \
      org.opencontainers.image.version="2.6.0" \
      org.opencontainers.image.vendor="HackMD" \
      org.opencontainers.image.source="https://github.com/hackmdio/hackmd-ce" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
