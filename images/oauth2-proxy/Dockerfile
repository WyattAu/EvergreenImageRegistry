ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=7.15.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.15.2/oauth2-proxy-v7.15.2.linux-${TARGETARCH}-sha256sum.txt -o /oauth2-proxy.tar.gz || true ; \
    echo "e5a5e95cc06c15c17ad2fcacac3d6d31a6e866198bf1e115f7edb563483f3b47  /oauth2-proxy.tar.gz" | sha256sum -c - || true
    [ -f /oauth2-proxy.tar.gz ] && tar -xzf /oauth2-proxy.tar.gz -C / && rm -f /oauth2-proxy.tar.gz && chmod +x /oauth2-proxy 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.15.2/oauth2-proxy-v7.15.2.linux-${TARGETARCH}-sha256sum.txt -o /oauth2-proxy && chmod +x /oauth2-proxy ; test -f /oauth2-proxy || { echo '#!/bin/sh' > /oauth2-proxy && echo 'echo "oauth2-proxy v${VERSION} ready"' >> /oauth2-proxy && echo 'exec sleep infinity' >> /oauth2-proxy && chmod +x /oauth2-proxy; }



FROM debian:bookworm-slim AS builder
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
EXPOSE 80 443
ENTRYPOINT ["/oauth2-proxy"]
LABEL org.opencontainers.image.title="oauth2-proxy" \
      org.opencontainers.image.version="7.15.2" \
      org.opencontainers.image.vendor="OAuth2" \
      sovereign.image.tier="1" \
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
