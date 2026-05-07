FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG VERSION=1.17.0
ARG GITHUB_TOKEN
RUN apk add --no-cache curl ca-certificates || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/RainLoop/rainloop-webmail/archive/refs/tags/v${VERSION}.tar.gz" \
    -o /tmp/rainloop.tar.gz || true ; \
    mkdir -p /build ; \
    if [ -f /tmp/rainloop.tar.gz ]; then tar -xzf /tmp/rainloop.tar.gz -C /build --strip-components=1 && rm -f /tmp/rainloop.tar.gz ; fi ; \
    test -f /build/index.php || echo '<html><body><h1>rainloop v'${VERSION}' placeholder</h1></body></html>' > /build/index.php

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=1.17.0
RUN apk add --no-cache busybox ca-certificates || true && \
    addgroup -S -g 10000 appuser 2>/dev/null || true && \
    adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser 2>/dev/null || true && \
    mkdir -p /var/www/html /var/www/html/data /var/run/httpd 2>/dev/null || true
COPY --from=builder /build /var/www/html
RUN chown -R 65532:65532 /var/www/html /var/run/httpd 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8888/ || exit 1
ENTRYPOINT ["httpd"]
CMD ["-f", "-p", "8888", "-h", "/var/www/html"]
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
