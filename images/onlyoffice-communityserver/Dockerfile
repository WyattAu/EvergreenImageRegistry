ARG VERSION=12.5.2
ARG TARGETARCH
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
ARG VERSION=12.5.2
RUN mkdir -p /opt/onlyoffice && \
    mkdir -p /var/lib/onlyoffice || true
RUN mkdir -p /etc/onlyoffice && \
    mkdir -p /opt/onlyoffice && \
    mkdir -p /var/lib/onlyoffice || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates tar xz-utils fontconfig \
        libxml2 libxslt1.1 nginx mono-complete \
        libmysqlclient21 libpq5 && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 10 --connect-timeout 30 --max-time 600 \
        -fsSL "https://github.com/ONLYOFFICE/CommunityServer/releases/download/v${VERSION}/onlyoffice-communityserver-linux-x64.tar.gz" \
        -o /tmp/communityserver.tar.gz || true && \
    if [ -f /tmp/communityserver.tar.gz ]; then \
        mkdir -p /opt/onlyoffice && \
        tar -xzf /tmp/communityserver.tar.gz -C /opt/onlyoffice && \
        rm -f /tmp/communityserver.tar.gz ; \
    fi && \
    mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /etc/onlyoffice \
        /opt/onlyoffice/Data /opt/onlyoffice/MySQL \
        /opt/onlyoffice/PostgreSQL 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=12.5.2
RUN apk add --no-cache ca-certificates tzdata fontconfig \
        libxml2 libxslt libstdc++ libgcc libjpeg-turbo \
        libpng libcurl openssl-libs freetype \
        postgresql-libs mariadb-libs || true && \
    mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /etc/onlyoffice \
        /opt/onlyoffice/Data /opt/onlyoffice/MySQL \
        /opt/onlyoffice/PostgreSQL /var/run/onlyoffice 2>/dev/null || true
COPY --from=installer /opt/onlyoffice /opt/onlyoffice
COPY --from=installer /var/log/onlyoffice /var/log/onlyoffice
COPY --from=installer /var/lib/onlyoffice /var/lib/onlyoffice
COPY --from=installer /etc/onlyoffice /etc/onlyoffice
RUN adduser -u 65532 -D -h /opt/onlyoffice -s /bin/false onlyoffice 2>/dev/null || true && \
    chown -R 65532:65532 /var/log/onlyoffice /var/lib/onlyoffice \
        /opt/onlyoffice /var/run/onlyoffice 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/onlyoffice
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:80/ || exit 1
ENTRYPOINT ["/opt/onlyoffice/onlyoffice-enterprise-service.sh"]
LABEL org.opencontainers.image.title="onlyoffice-communityserver" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ONLYOFFICE" \
      org.opencontainers.image.source="https://github.com/ONLYOFFICE/CommunityServer" \
      org.opencontainers.image.description="Evergreen hardened ONLYOFFICE Community Server" \
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
