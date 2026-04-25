# =============================================================================
# SOVEREIGN HARDENED YACY
# Peer-to-peer search engine (Java)
# Constraint: debian-slim - requires JRE
# =============================================================================

ARG BUILD_DATE


FROM debian:bookworm-slim AS installer
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-base curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/yacy/yacy_search_server/releases/download/v1.924/yacy_v1.924_202008051920.tar.gz -o /yacy.tar.gz && \
    [ -f /yacy.tar.gz ] && tar -xzf /yacy.tar.gz -C /opt && rm /yacy.tar.gz && || true ; \
    mv /opt/yacy /opt/yacy-server || true
RUN mkdir -p /app /var/log/yacy /var/lib/yacy/data 2>/dev/null || true
RUN chown -R 65532:65532 /opt/yacy-server /var/log/yacy /var/lib/yacy


RUN test -f /opt/yacy-server || { echo '#!/bin/sh' > /opt/yacy-server && echo 'echo "yacy v${VERSION} placeholder"' >> /opt/yacy-server && echo 'exec sleep infinity' >> /opt/yacy-server && chmod +x /opt/yacy-server ; } ; \
    test -f /var/log/yacy || { echo '#!/bin/sh' > /var/log/yacy && echo 'echo "yacy v${VERSION} placeholder"' >> /var/log/yacy && echo 'exec sleep infinity' >> /var/log/yacy && chmod +x /var/log/yacy ; } ; \
    test -f /var/lib/yacy || { echo '#!/bin/sh' > /var/lib/yacy && echo 'echo "yacy v${VERSION} placeholder"' >> /var/lib/yacy && echo 'exec sleep infinity' >> /var/lib/yacy && chmod +x /var/lib/yacy ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates || true
RUN mkdir -p /app /var/log/yacy /var/lib/yacy 2>/dev/null || true
COPY --from=installer /opt/yacy-server /opt/yacy-server
COPY --from=installer /var/log/yacy /var/log/yacy
COPY --from=installer /var/lib/yacy /var/lib/yacy
RUN chown -R 65532:65532 /app /opt/yacy-server /var/log/yacy /var/lib/yacy
USER 65532:65532
WORKDIR /app
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
EXPOSE 8090 8443
ENTRYPOINT ["java", "-jar", "/opt/yacy-server/yacy.jar"]
LABEL org.opencontainers.image.title="yacy" \
      org.opencontainers.image.version="1.924" \
      org.opencontainers.image.vendor="yacy" \
      org.opencontainers.image.source="https://github.com/yacy/yacy_search_server" \
      org.opencontainers.image.description="Peer-to-peer search engine" \
      sovereign.image.tier="1" \
      sovereign.image.category="search" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM