ARG VERSION=12.5.2
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
ARG VERSION=12.5.2
RUN mkdir -p /opt/onlyoffice/controlpanel && \
    mkdir -p /var/lib/onlyoffice || true
RUN mkdir -p /etc/onlyoffice && \
    mkdir -p /opt/onlyoffice/controlpanel && \
    mkdir -p /var/lib/onlyoffice || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates tar xz-utils fontconfig \
        libxml2 libxslt1.1 mono-complete && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 10 --connect-timeout 30 --max-time 600 \
        -fsSL "https://github.com/ONLYOFFICE/CommunityServer/releases/download/v${VERSION}/onlyoffice-controlpanel-linux-x64.tar.gz" \
        -o /tmp/controlpanel.tar.gz && \
    if [ -f /tmp/controlpanel.tar.gz ]; then \
        mkdir -p /opt/onlyoffice/controlpanel && \
        tar -xzf /tmp/controlpanel.tar.gz -C /opt/onlyoffice/controlpanel && \
        rm -f /tmp/controlpanel.tar.gz ; \
    fi && \
    mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /etc/onlyoffice \
        /opt/onlyoffice/controlpanel/Data 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=12.5.2
RUN apk add --no-cache ca-certificates tzdata fontconfig libxml2 libxslt libstdc++ libgcc libjpeg-turbo libpng libcurl freetype &&  mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /etc/onlyoffice  /opt/onlyoffice/controlpanel/Data /var/run/onlyoffice 2>/dev/null
COPY --from=installer /opt/onlyoffice/controlpanel /opt/onlyoffice/controlpanel
COPY --from=installer /var/log/onlyoffice /var/log/onlyoffice
COPY --from=installer /var/lib/onlyoffice /var/lib/onlyoffice
COPY --from=installer /etc/onlyoffice /etc/onlyoffice
RUN adduser -u 65532 -D -h /opt/onlyoffice/controlpanel -s /bin/false onlyoffice 2>/dev/null || true && \
    chown -R 65532:65532 /var/log/onlyoffice /var/lib/onlyoffice \
        /opt/onlyoffice/controlpanel /var/run/onlyoffice 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/onlyoffice/controlpanel
EXPOSE 80 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
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
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
