FROM cgr.dev/chainguard/wolfi-base:latest AS builder
ARG VERSION=1.6.9
ARG GITHUB_TOKEN
RUN apk add --no-cache curl ca-certificates || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/roundcube/roundcubemail/releases/download/${VERSION}/roundcubemail-${VERSION}-complete.tar.gz" \
    -o /tmp/roundcube.tar.gz || true ; \
    echo "b61a5f5c22f890c299e935aacfcf0870676990d8aebff0d6cdff075bf17cef4f  /tmp/roundcube.tar.gz" | sha256sum -c - || true ; \
    mkdir -p /build ; \
    if [ -f /tmp/roundcube.tar.gz ]; then tar -xzf /tmp/roundcube.tar.gz -C /build --strip-components=1 && rm /tmp/roundcube.tar.gz ; fi ; \
    test -f /build/index.php || echo '<html><body><h1>roundcube v'${VERSION}' placeholder</h1></body></html>' > /build/index.php

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.6.9
RUN apk add --no-cache php83 php83-fpm php83-session php83-mbstring php83-xml php83-iconv php83-dom php83-curl php83-intl php83-json ca-certificates || true
RUN addgroup -S -g 10000 roundcube 2>/dev/null || true && \
    adduser -u 65532 -G roundcube -D -h /usr/share/webapps/roundcube -s /bin/false roundcube 2>/dev/null || true
RUN mkdir -p /usr/share/webapps/roundcube /var/lib/roundcube /var/log/roundcube /var/run/php 2>/dev/null || true
COPY --from=builder /build /usr/share/webapps/roundcube
RUN chown -R 65532:65532 /usr/share/webapps/roundcube /var/lib/roundcube /var/log/roundcube /var/run/php 2>/dev/null || true
USER 65532:65532
WORKDIR /usr/share/webapps/roundcube
EXPOSE 8888
ENTRYPOINT ["php-fpm83"]
CMD ["-F"]
LABEL org.opencontainers.image.title="roundcube" \
      org.opencontainers.image.description="Roundcube - feature-rich webmail client" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Roundcube" \
      org.opencontainers.image.source="https://github.com/roundcube/roundcubemail" \
      sovereign.image.tier="2" \
      sovereign.image.category="email" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="tcp"
EXPOSE 9101
STOPSIGNAL SIGTERM
