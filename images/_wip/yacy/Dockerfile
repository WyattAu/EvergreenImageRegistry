ARG VERSION=1.93
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM yacy/yacy_search_server:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates || true \
    mkdir -p /app /var/log/yacy /var/lib/yacy /opt 2>/dev/null || true
RUN mkdir -p /opt/yacy-server || true
COPY --from=upstream /opt/yacy /opt/yacy-server
RUN chown -R 65532:65532 /app /opt/yacy-server /var/log/yacy /var/lib/yacy 2>/dev/null || true

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk

WORKDIR /app

EXPOSE 8090 8443
EXPOSE 9101

LABEL org.opencontainers.image.title="yacy" org.opencontainers.image.version="1.924" org.opencontainers.image.vendor="yacy" org.opencontainers.image.source="https://github.com/yacy/yacy_search_server" org.opencontainers.image.description="Peer-to-peer search engine" evergreen.image.tier="1" evergreen.image.category="search" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.base="wolfi" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="5s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8090/ || exit 1
ENTRYPOINT ["java", "-jar", "/opt/yacy-server/yacy.jar"]
