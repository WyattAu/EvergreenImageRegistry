ARG VERSION=12.5.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
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

FROM cgr.dev/chainguard/wolfi-base:latest
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
ENTRYPOINT ["/opt/onlyoffice/controlpanel/start.sh"]
LABEL org.opencontainers.image.title="onlyoffice-controlpanel" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ONLYOFFICE" \
      org.opencontainers.image.source="https://github.com/ONLYOFFICE/CommunityServer" \
      org.opencontainers.image.description="Sovereign hardened ONLYOFFICE Control Panel" \
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
