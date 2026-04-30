ARG VERSION=8.3.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gdebi-core fontconfig \
        libxml2-utils libxslt1.1 libcairo2 libglib2.0-0 \
        libjpeg62-turbo libpng16-16 libtiff5 libpoppler97 \
        libpq5 libcurl4 libssl3 fonts-liberation fonts-dejavu \
        fonts-crosextra-carlito fonts-takao-gothic && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 10 --connect-timeout 30 --max-time 600 \
        -fsSL "https://download.onlyoffice.com/documentserver/linux/onlyoffice-documentserver-amd64.deb" \
        -o /tmp/onlyoffice-documentserver.deb || true
RUN if [ -f /tmp/onlyoffice-documentserver.deb ]; then \
        gdebi --non-interactive /tmp/onlyoffice-documentserver.deb || \
        dpkg -i --force-depends /tmp/onlyoffice-documentserver.deb || true ; \
        rm -f /tmp/onlyoffice-documentserver.deb ; \
    fi
RUN mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /var/www/onlyoffice \
        /etc/onlyoffice /usr/lib/onlyoffice /opt/onlyoffice 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates tzdata fontconfig \
        libxml2 libxslt libstdc++ libgcc libjpeg-turbo \
        libpng libtiff libwebp libcurl openssl-libs \
        freetype harfbuzz graphite2 bzip2-libs zlib \
        postgresql-libs glib || true
RUN mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /var/www/onlyoffice \
        /etc/onlyoffice /usr/lib/onlyoffice /opt/onlyoffice \
        /var/run/onlyoffice 2>/dev/null || true
COPY --from=installer /var/log/onlyoffice /var/log/onlyoffice
COPY --from=installer /var/lib/onlyoffice /var/lib/onlyoffice
COPY --from=installer /var/www/onlyoffice /var/www/onlyoffice
COPY --from=installer /etc/onlyoffice /etc/onlyoffice
COPY --from=installer /usr/lib/onlyoffice /usr/lib/onlyoffice
COPY --from=installer /opt/onlyoffice /opt/onlyoffice
COPY --from=installer /usr/bin/ds /usr/bin/ds 2>/dev/null || true
RUN adduser -u 65532 -D -h /var/lib/onlyoffice -s /bin/false onlyoffice 2>/dev/null || true && \
    chown -R 65532:65532 /var/log/onlyoffice /var/lib/onlyoffice \
        /var/www/onlyoffice /var/run/onlyoffice 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/onlyoffice
EXPOSE 80 443
ENTRYPOINT ["/usr/bin/ds", "--foreground"]
LABEL org.opencontainers.image.title="onlyoffice-documentserver" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ONLYOFFICE" \
      org.opencontainers.image.source="https://github.com/ONLYOFFICE/DocumentServer" \
      org.opencontainers.image.description="Sovereign hardened ONLYOFFICE Document Server" \
      sovereign.image.tier="2" \
      sovereign.image.category="document-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
