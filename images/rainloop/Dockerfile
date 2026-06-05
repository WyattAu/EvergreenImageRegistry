ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG VERSION=1.17.0
ARG TARGETARCH
RUN mkdir -p /build || true
RUN apk add --no-cache curl ca-certificates
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/RainLoop/rainloop-webmail/archive/refs/tags/v${VERSION}.tar.gz" \
    -o /tmp/rainloop.tar.gz ; \
    mkdir -p /build ; \
    if [ -f /tmp/rainloop.tar.gz ]; then tar -xzf /tmp/rainloop.tar.gz -C /build --strip-components=1 && rm -f /tmp/rainloop.tar.gz ; fi ; \
    test -s /build/index.php || echo '<html><body><h1>rainloop v'${VERSION}' && { echo "Binary not available - download failed" >&2; exit 1; }

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=1.17.0
RUN apk add --no-cache busybox ca-certificates && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true && \
    mkdir -p /var/www/html /var/www/html/data /var/run/httpd 2>/dev/null || true
COPY --from=builder /build /var/www/html
RUN chown -R 65532:65532 /var/www/html /var/run/httpd 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 8888

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8888"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "httpd", "--", "-f", "-p", "8888", "-h", "/var/www/html"]
LABEL org.opencontainers.image.title="rainloop" \
      org.opencontainers.image.description="RainLoop - lightweight webmail client" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="RainLoop" \
      org.opencontainers.image.source="https://github.com/RainLoop/rainloop-webmail" \
      evergreen.image.tier="2" \
      evergreen.image.category="email" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
