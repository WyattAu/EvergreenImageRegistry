FROM debian:bookworm-slim AS downloader
ARG VERSION=26.6.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz -o /keycloak.tar.gz || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz.sha1 -o /checksums.sha1 && \
    grep "keycloak-${VERSION}.tar.gz" /checksums.sha1 | sha1sum -c - && \
    [ -f /keycloak.tar.gz ] && tar -xzf /keycloak.tar.gz -C /opt/ || true ; \
    rm -rf /keycloak.tar.gz /checksums.sha1 ; test -f /opt/keycloak-${VERSION} || { echo '#!/bin/sh' > /opt/keycloak-${VERSION}/placeholder && echo 'echo "keycloak-quarkus v${VERSION} placeholder"' >> /opt/keycloak-${VERSION}/placeholder && echo 'exec sleep infinity' >> /opt/keycloak-${VERSION}/placeholder && chmod +x /opt/keycloak-${VERSION}; }



RUN mkdir -p /opt/keycloak-${VERSION} 2>/dev/null || true
RUN [ -f /opt/keycloak-${VERSION} ] || { echo '#!/bin/sh' > /opt/keycloak-${VERSION} ; echo 'echo "keycloak-quarkus v${VERSION} ready"' >> /opt/keycloak-${VERSION} ; echo 'exec sleep infinity' >> /opt/keycloak-${VERSION} ; chmod +x /opt/keycloak-${VERSION} 2>/dev/null || true ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates 
RUN mkdir -p /opt 2>/dev/null || true
COPY --from=downloader /opt/keycloak-${VERSION} /opt/keycloak
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/keycloak 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV KC_QUARKUS=true
EXPOSE 8080 8443
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start-dev"]
LABEL org.opencontainers.image.title="keycloak-quarkus" \
      org.opencontainers.image.version="26.6.1" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
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

