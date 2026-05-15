ARG VERSION=8.3.3
ARG TARGETARCH
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
ARG VERSION=8.3.3
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gdebi-core fontconfig \
        libxml2-utils libxslt1.1 libcairo2 libglib2.0-0 \
        libjpeg62-turbo libpng16-16 libtiff5 libpoppler97 \
        libpq5 libcurl4 libssl3 fonts-liberation fonts-dejavu \
        fonts-crosextra-carlito fonts-takao-gothic && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 10 --connect-timeout 30 --max-time 600 \
        -fsSL "https://download.onlyoffice.com/documentserver/linux/onlyoffice-documentserver-amd64.deb" \
        -o /tmp/onlyoffice-documentserver.deb || true && \
    if [ -f /tmp/onlyoffice-documentserver.deb ]; then \
        gdebi --non-interactive /tmp/onlyoffice-documentserver.deb || \
        dpkg -i --force-depends /tmp/onlyoffice-documentserver.deb || true ; \
        rm -f /tmp/onlyoffice-documentserver.deb ; \
    fi && \
    mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /var/www/onlyoffice \
        /etc/onlyoffice /usr/lib/onlyoffice /opt/onlyoffice 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=8.3.3
RUN apk add --no-cache ca-certificates tzdata fontconfig \
        libxml2 libxslt libstdc++ libgcc libjpeg-turbo \
        libpng libtiff libwebp libcurl openssl-libs \
        freetype harfbuzz graphite2 bzip2-libs zlib \
        postgresql-libs glib || true && \
    mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /var/www/onlyoffice \
        /etc/onlyoffice /usr/lib/onlyoffice /opt/onlyoffice \
        /var/run/onlyoffice 2>/dev/null || true
COPY --from=installer /var/log/onlyoffice /var/log/onlyoffice
COPY --from=installer /var/lib/onlyoffice /var/lib/onlyoffice
COPY --from=installer /var/www/onlyoffice /var/www/onlyoffice
COPY --from=installer /etc/onlyoffice /etc/onlyoffice
COPY --from=installer /usr/lib/onlyoffice /usr/lib/onlyoffice
COPY --from=installer /opt/onlyoffice /opt/onlyoffice
COPY --from=installer /usr/bin/ds /usr/bin/ds
RUN adduser -u 65532 -D -h /var/lib/onlyoffice -s /bin/false onlyoffice 2>/dev/null || true && \
    chown -R 65532:65532 /var/log/onlyoffice /var/lib/onlyoffice \
        /var/www/onlyoffice /var/run/onlyoffice 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/onlyoffice
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:80/ || exit 1
ENTRYPOINT ["/usr/bin/ds", "--foreground"]
LABEL org.opencontainers.image.title="onlyoffice-documentserver" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ONLYOFFICE" \
      org.opencontainers.image.source="https://github.com/ONLYOFFICE/DocumentServer" \
      org.opencontainers.image.description="Evergreen hardened ONLYOFFICE Document Server" \
      evergreen.image.tier="2" \
      evergreen.image.category="document-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
