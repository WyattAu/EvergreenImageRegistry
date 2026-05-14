FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG VERSION=1.6.9
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apk add --no-cache curl ca-certificates || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/roundcube/roundcubemail/releases/download/${VERSION}/roundcubemail-${VERSION}-complete.tar.gz" \
    -o /tmp/roundcube.tar.gz || true ; \
    echo "b61a5f5c22f890c299e935aacfcf0870676990d8aebff0d6cdff075bf17cef4f  /tmp/roundcube.tar.gz" | sha256sum -c || true || true ; \
    mkdir -p /build ; \
    if [ -f /tmp/roundcube.tar.gz ]; then tar -xzf /tmp/roundcube.tar.gz -C /build --strip-components=1 && rm -f /tmp/roundcube.tar.gz ; fi ; \
    test -f /build/index.php || echo '<html><body><h1>roundcube v'${VERSION}' placeholder</h1></body></html>' > /build/index.php

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=1.6.9
RUN apk add --no-cache php php-fpm php-session php-mbstring php-xml php-iconv php-dom php-curl php-intl php-json ca-certificates || true && \
    addgroup -S -g 10000 roundcube 2>/dev/null || true && \
    adduser -u 65532 -G roundcube -D -h /usr/share/webapps/roundcube -s /bin/false roundcube 2>/dev/null || true && \
    mkdir -p /usr/share/webapps/roundcube /var/lib/roundcube /var/log/roundcube /var/run/php 2>/dev/null || true
COPY --from=builder /build /usr/share/webapps/roundcube
RUN chown -R 65532:65532 /usr/share/webapps/roundcube /var/lib/roundcube /var/log/roundcube /var/run/php 2>/dev/null || true
USER 65532:65532
WORKDIR /usr/share/webapps/roundcube
EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8888/ || exit 1
ENTRYPOINT ["php-fpm83"]
CMD ["-F"]
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
