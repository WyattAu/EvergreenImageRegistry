ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG VERSION=4.2.2
ARG TARGETARCH
RUN mkdir -p /www || true
RUN apk add --no-cache curl ca-certificates && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/cinnyapp/cinny/releases/download/v${VERSION}/cinny-v${VERSION}.tar.gz" \
    -o /tmp/cinny.tar.gz ; \
    echo "231627eea91fe28f0ea0b954ef21509cb42c91e2472617ddeed3a0d6c231b8c8  /tmp/cinny.tar.gz" | sha256sum -c ; \
    mkdir -p /www ; \
    if [ -f /tmp/cinny.tar.gz ]; then tar -xzf /tmp/cinny.tar.gz -C /www --strip-components=1 && rm -f /tmp/cinny.tar.gz ; fi ; \
    test -s /www/index.html || echo '<html><body><h1>cinny v'${VERSION}' binary not available - download failed" >&2 exit 1</h1></body></html>' > /www/index.html
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache busybox ca-certificates && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true && \
    mkdir -p /var/www/html /var/run/httpd 2>/dev/null || true
COPY --from=builder /www /var/www/html
RUN chown -R 65532:65532 /var/www/html /var/run/httpd 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "httpd", "--", "-f", "-p", "80", "-h", "/var/www/html"]
LABEL org.opencontainers.image.title="cinny" \
      org.opencontainers.image.description="Cinny - lightweight Matrix web client" \
      org.opencontainers.image.version="4.2.2" \
      org.opencontainers.image.vendor="Cinny" \
      org.opencontainers.image.source="https://github.com/cinnyapp/cinny" \
      evergreen.image.tier="2" \
      evergreen.image.category="chat" \
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
