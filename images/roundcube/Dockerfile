ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG VERSION=1.6.9
ARG TARGETARCH
RUN mkdir -p /build || true
RUN apk add --no-cache curl ca-certificates
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/roundcube/roundcubemail/releases/download/${VERSION}/roundcubemail-${VERSION}-complete.tar.gz" \
    -o /tmp/roundcube.tar.gz ; \
    echo "b61a5f5c22f890c299e935aacfcf0870676990d8aebff0d6cdff075bf17cef4f  /tmp/roundcube.tar.gz" | sha256sum -c ; \
    mkdir -p /build ; \
    if [ -f /tmp/roundcube.tar.gz ]; then tar -xzf /tmp/roundcube.tar.gz -C /build --strip-components=1 && rm -f /tmp/roundcube.tar.gz ; fi ; \
    test -s /build/index.php || echo '<html><body><h1>roundcube v'${VERSION}' && { echo "Binary not available - download failed" >&2; exit 1; }

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=1.6.9
RUN apk add --no-cache php-8.4 php-8.4-fpm php-8.4-session php-8.4-mbstring php-8.4-xml php-8.4-iconv php-8.4-dom php-8.4-curl php-8.4-intl ca-certificates && \
    addgroup -S -g 10000 roundcube 2>/dev/null || true && \
    adduser -u 65532 -G roundcube -D -h /usr/share/webapps/roundcube -s /bin/false roundcube 2>/dev/null || true && \
    mkdir -p /usr/share/webapps/roundcube /var/lib/roundcube /var/log/roundcube /var/run/php-8.4 2>/dev/null || true
COPY --from=builder /build /usr/share/webapps/roundcube
RUN chown -R 65532:65532 /usr/share/webapps/roundcube /var/lib/roundcube /var/log/roundcube /var/run/php 2>/dev/null || true
USER 65532:65532
WORKDIR /usr/share/webapps/roundcube
EXPOSE 8888

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8888"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "php-fpm83", "--", "-F"]
LABEL org.opencontainers.image.title="roundcube" \
      org.opencontainers.image.description="Roundcube - feature-rich webmail client" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Roundcube" \
      org.opencontainers.image.source="https://github.com/roundcube/roundcubemail" \
      evergreen.image.tier="2" \
      evergreen.image.category="email" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
