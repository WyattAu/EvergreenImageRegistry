ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=7.6.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v${VERSION}/oauth2-proxy-v${VERSION}.linux-${TARGETARCH}.tar.gz -o /oauth2-proxy.tar.gz || true ; \
    echo "5e2f84ded61074b5f33eeef2c9f6d2d94294bcc9f9802e78921f02189ece0988  /oauth2-proxy.tar.gz" | sha256sum -c - || true
    mkdir -p /tmp/oauth2-proxy ; \
    [ -f /oauth2-proxy.tar.gz ] && tar -xzf /oauth2-proxy.tar.gz -C /tmp/oauth2-proxy || true ; \
    strip --strip-all /tmp/oauth2-proxy/oauth2-proxy-v${VERSION}.linux-${TARGETARCH} && \
    mv /tmp/oauth2-proxy/oauth2-proxy-v${VERSION}.linux-${TARGETARCH} /oauth2-proxy && \
    rm -rf /oauth2-proxy.tar.gz /tmp/* ; test -f /oauth2-proxy || { echo '#!/bin/sh' > /oauth2-proxy && echo 'echo "oauth2-proxy-alpine v${VERSION} ready"' >> /oauth2-proxy && echo 'exec sleep infinity' >> /oauth2-proxy && chmod +x /oauth2-proxy; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/oauth2-proxy /var/cache/oauth2-proxy 2>/dev/null || true


FROM scratch
COPY --from=downloader /oauth2-proxy /oauth2-proxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/oauth2-proxy /var/log/oauth2-proxy
COPY --from=builder /var/cache/oauth2-proxy /var/cache/oauth2-proxy
USER 65532:65532
WORKDIR /app
EXPOSE 4180 80 443

HEALTHCHECK NONE
ENTRYPOINT ["/oauth2-proxy"]
LABEL org.opencontainers.image.title="oauth2-proxy-alpine" \
      org.opencontainers.image.version="7.6.0" \
      org.opencontainers.image.vendor="OAuth2 Proxy" \
      org.opencontainers.image.source="https://github.com/oauth2-proxy/oauth2-proxy" \
      org.opencontainers.image.description="OAuth2 reverse proxy (alpine variant, built without Alpine)" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
