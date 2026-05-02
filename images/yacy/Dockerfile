ARG VERSION=latest

FROM yacy/yacy_search_server:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
RUN mkdir -p /app /var/log/yacy /var/lib/yacy /opt 2>/dev/null || true
COPY --from=upstream /opt/yacy /opt/yacy-server
RUN chown -R 65532:65532 /app /opt/yacy-server /var/log/yacy /var/lib/yacy 2>/dev/null || true

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk

WORKDIR /app

EXPOSE 8090 8443
EXPOSE 9101

LABEL org.opencontainers.image.title="yacy" org.opencontainers.image.version="1.924" org.opencontainers.image.vendor="yacy" org.opencontainers.image.source="https://github.com/yacy/yacy_search_server" org.opencontainers.image.description="Peer-to-peer search engine" sovereign.image.tier="1" sovereign.image.category="search" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.base="wolfi" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="5s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["java", "-jar", "/opt/yacy-server/yacy.jar"]
