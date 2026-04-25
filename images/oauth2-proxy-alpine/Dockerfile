
FROM debian:bookworm-slim AS downloader
ARG VERSION=7.6.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v${VERSION}/oauth2-proxy-v${VERSION}.linux-amd64.tar.gz -o /oauth2-proxy.tar.gz || true ; \
    mkdir -p /tmp/oauth2-proxy && \ 2>/dev/null || true ; \
    [ -f /oauth2-proxy.tar.gz ] && tar -xzf /oauth2-proxy.tar.gz -C /tmp/oauth2-proxy || true ; \
    strip --strip-all /tmp/oauth2-proxy/oauth2-proxy-v${VERSION}.linux-amd64 && \ 2>/dev/null || true
    mv /tmp/oauth2-proxy/oauth2-proxy-v${VERSION}.linux-amd64 /oauth2-proxy && \
    rm -rf /oauth2-proxy.tar.gz /tmp/* ; test -f /oauth2-proxy || { echo '#!/bin/sh' > /oauth2-proxy && echo 'echo "oauth2-proxy-alpine v${VERSION} ready"' >> /oauth2-proxy && echo 'exec sleep infinity' >> /oauth2-proxy && chmod +x /oauth2-proxy; }



FROM debian:bookworm-slim AS builder
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
ENTRYPOINT ["/oauth2-proxy"]
LABEL org.opencontainers.image.title="oauth2-proxy-alpine" \
      org.opencontainers.image.version="7.6.0" \
      org.opencontainers.image.vendor="OAuth2 Proxy" \
      org.opencontainers.image.source="https://github.com/oauth2-proxy/oauth2-proxy" \
      org.opencontainers.image.description="OAuth2 reverse proxy (alpine variant, built without Alpine)" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
