ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG VERSION=2.6.1
ARG TARGETARCH
RUN mkdir -p /build || true
RUN apk add --no-cache nodejs-20 npm git ca-certificates python3 make gcc
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/hackmdio/codimd/releases/download/${VERSION}/codimd-${VERSION}.tar.gz" \
    -o /tmp/codimd.tar.gz ; \
    mkdir -p /build ; \
    if [ -f /tmp/codimd.tar.gz ]; then tar -xzf /tmp/codimd.tar.gz -C /build --strip-components=1 && rm -f /tmp/codimd.tar.gz ; fi && \
    cd /build && npm ci 2>/dev/null || npm install --legacy-peer-deps 2>/dev/null && \
    npm run build 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=2.6.1
RUN apk add --no-cache nodejs-20 npm ca-certificates && \
    addgroup -S -g 10000 codimd 2>/dev/null || true && \
    adduser -u 65532 -G codimd -D -h /app -s /bin/false codimd 2>/dev/null || true && \
    mkdir -p /app/codimd /var/log/codimd /app/codimd/data 2>/dev/null || true
COPY --from=builder /build /app/codimd
RUN chown -R 65532:65532 /app/codimd /var/log/codimd 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app/codimd
ENV NODE_ENV="production"
EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "node", "--", "./app.js"]
LABEL org.opencontainers.image.title="codimd" \
      org.opencontainers.image.description="CodiMD - collaborative markdown editor" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="hackmdio" \
      org.opencontainers.image.source="https://github.com/hackmdio/codimd" \
      evergreen.image.tier="2" \
      evergreen.image.category="collaboration" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
