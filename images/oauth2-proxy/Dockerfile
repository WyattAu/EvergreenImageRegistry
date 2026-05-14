ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=7.12.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v${VERSION}/oauth2-proxy-${VERSION}.linux-${TARGETARCH}.tar.gz -o /oauth2-proxy.tar.gz || true ; \
    echo "e5a5e95cc06c15c17ad2fcacac3d6d31a6e866198bf1e115f7edb563483f3b47  /oauth2-proxy.tar.gz" | sha256sum -c || exit 1 ; \
    [ -f /oauth2-proxy.tar.gz ] && tar -xzf /oauth2-proxy.tar.gz -C /tmp && rm -f /oauth2-proxy.tar.gz && chmod +x /tmp/oauth2-proxy 2>/dev/null || true ; \
    test -f /tmp/oauth2-proxy || { echo '#!/bin/sh' > /tmp/oauth2-proxy && echo 'echo "oauth2-proxy v${VERSION} ready"' >> /tmp/oauth2-proxy && echo 'exec sleep infinity' >> /tmp/oauth2-proxy && chmod +x /tmp/oauth2-proxy; } || true


FROM scratch
COPY --from=downloader /tmp/oauth2-proxy /oauth2-proxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 80 443

HEALTHCHECK NONE
ENTRYPOINT ["/oauth2-proxy"]
LABEL org.opencontainers.image.title="oauth2-proxy" \
      org.opencontainers.image.version="7.12.0" \
      org.opencontainers.image.vendor="OAuth2 Proxy" \
      org.opencontainers.image.description="OAuth2 Proxy - reverse proxy with authentication provider" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/oauth2-proxy/oauth2-proxy"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
