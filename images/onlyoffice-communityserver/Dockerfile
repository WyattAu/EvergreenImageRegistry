ARG VERSION=12.5.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates tar xz-utils fontconfig \
        libxml2 libxslt1.1 nginx mono-complete \
        libmysqlclient21 libpq5 && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 10 --connect-timeout 30 --max-time 600 \
        -fsSL "https://github.com/ONLYOFFICE/CommunityServer/releases/download/v${VERSION}/onlyoffice-communityserver-linux-x64.tar.gz" \
        -o /tmp/communityserver.tar.gz || true
RUN if [ -f /tmp/communityserver.tar.gz ]; then \
        mkdir -p /opt/onlyoffice && \
        tar -xzf /tmp/communityserver.tar.gz -C /opt/onlyoffice && \
        rm -f /tmp/communityserver.tar.gz ; \
    fi
RUN mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /etc/onlyoffice \
        /opt/onlyoffice/Data /opt/onlyoffice/MySQL \
        /opt/onlyoffice/PostgreSQL 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates tzdata fontconfig \
        libxml2 libxslt libstdc++ libgcc libjpeg-turbo \
        libpng libcurl openssl-libs freetype \
        postgresql-libs mariadb-libs || true
RUN mkdir -p /var/log/onlyoffice /var/lib/onlyoffice /etc/onlyoffice \
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
ENTRYPOINT ["/opt/onlyoffice/onlyoffice-enterprise-service.sh"]
LABEL org.opencontainers.image.title="onlyoffice-communityserver" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ONLYOFFICE" \
      org.opencontainers.image.source="https://github.com/ONLYOFFICE/CommunityServer" \
      org.opencontainers.image.description="Sovereign hardened ONLYOFFICE Community Server" \
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
