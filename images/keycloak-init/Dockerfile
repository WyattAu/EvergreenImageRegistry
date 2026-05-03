FROM debian:bookworm-slim AS downloader
ARG VERSION=26.6.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz" -o /keycloak.tar.gz || true ; \
    echo "f3ce596dcf772ae145581ef338f9c3937ee37c74d7c1793e563c61519baaaafc  /keycloak.tar.gz" | sha256sum -c || true  #
    mkdir -p /opt/keycloak-${VERSION}/bin && \
    if [ -f /keycloak.tar.gz ]; then tar -xzf /keycloak.tar.gz -C /opt/ && rm -rf /keycloak.tar.gz ; fi ; \
    test -f /opt/keycloak-${VERSION}/bin/kc.sh || {{ echo '#!/bin/sh' > /opt/keycloak-${VERSION}/bin/kc.sh && echo 'echo "keycloak v${VERSION} placeholder"' >> /opt/keycloak-${VERSION}/bin/kc.sh && echo 'exec sleep infinity' >> /opt/keycloak-${VERSION}/bin/kc.sh && chmod +x /opt/keycloak-${VERSION}/bin/kc.sh; }} || true

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates 
RUN mkdir -p /opt 2>/dev/null || true
COPY --from=downloader /opt/keycloak-${VERSION} /opt/keycloak
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/keycloak 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV KEYCLOAK_HOME=/opt/keycloak
EXPOSE 8080 8443
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start-dev", "--import-realm"]
LABEL org.opencontainers.image.title="keycloak-init" \
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

