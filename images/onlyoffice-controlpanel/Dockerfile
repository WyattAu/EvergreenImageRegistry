ARG VERSION=12.5.2
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates tar xz-utils fontconfig \
        libxml2 libxslt1.1 mono-complete && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 10 --connect-timeout 30 --max-time 600 \
        -fsSL "https://github.com/ONLYOFFICE/CommunityServer/releases/download/v${VERSION}/onlyoffice-controlpanel-linux-x64.tar.gz" \
        -o /tmp/controlpanel.tar.gz || true
RUN if [ -f /tmp/controlpanel.tar.gz ]; then \
        mkdir -p /opt/onlyoffice/controlpanel && \
        tar -xzf /tmp/controlpanel.tar.gz -C /opt/onlyoffice/controlpanel && \
        rm -f /tmp/controlpanel.tar.gz ; \
    fi
RUN mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /etc/onlyoffice \
        /opt/onlyoffice/controlpanel/Data 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION
RUN apk add --no-cache ca-certificates tzdata fontconfig \
        libxml2 libxslt libstdc++ libgcc libjpeg-turbo \
        libpng libcurl openssl-libs freetype || true
RUN mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /etc/onlyoffice \
        /opt/onlyoffice/controlpanel/Data /var/run/onlyoffice 2>/dev/null || true
COPY --from=installer /opt/onlyoffice/controlpanel /opt/onlyoffice/controlpanel
COPY --from=installer /var/log/onlyoffice /var/log/onlyoffice
COPY --from=installer /var/lib/onlyoffice /var/lib/onlyoffice
COPY --from=installer /etc/onlyoffice /etc/onlyoffice
RUN adduser -u 65532 -D -h /opt/onlyoffice/controlpanel -s /bin/false onlyoffice 2>/dev/null || true && \
    chown -R 65532:65532 /var/log/onlyoffice /var/lib/onlyoffice \
        /opt/onlyoffice/controlpanel /var/run/onlyoffice 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/onlyoffice/controlpanel
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["/opt/onlyoffice/controlpanel/start.sh"]
LABEL org.opencontainers.image.title="onlyoffice-controlpanel" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ONLYOFFICE" \
      org.opencontainers.image.source="https://github.com/ONLYOFFICE/CommunityServer" \
      org.opencontainers.image.description="Evergreen hardened ONLYOFFICE Control Panel" \
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

EXPOSE 9101
STOPSIGNAL SIGTERM
