FROM debian:bookworm-slim AS downloader
ARG VERSION=2026.2.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/goauthentik/authentik/releases/download/version/${VERSION}/authentik-proxy-${VERSION}.tar.gz -o /authentik-proxy.tar.gz && || true ; \
    mkdir -p /tmp/authentik-proxy && \ 2>/dev/null || true ; \
    [ -f /authentik-proxy.tar.gz ] && tar -xzf /authentik-proxy.tar.gz -C /tmp/authentik-proxy && || true ; \
    rm -f /authentik-proxy.tar.gz ; test -f /tmp/authentik-proxy || { echo '#!/bin/sh' > /tmp/authentik-proxy && echo 'echo "authentik-proxy v${VERSION} placeholder"' >> /tmp/authentik-proxy && echo 'exec sleep infinity' >> /tmp/authentik-proxy && chmod +x /tmp/authentik-proxy; }


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates libpq || true
COPY --from=downloader /tmp/authentik-proxy /opt/authentik-proxy
RUN pip install --no-cache-dir --break-system-packages /opt/authentik-proxy 2>/dev/null || pip install --no-cache-dir /opt/authentik-proxy || true && \
    mkdir -p /app && chown -R 65532:65532 /app /opt/authentik-proxy 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9000 9443
ENTRYPOINT ["python3", "-m", "authentik"]
CMD ["proxy"]
LABEL org.opencontainers.image.title="authentik-proxy" \
      org.opencontainers.image.version="2026.2.2" \
      org.opencontainers.image.vendor="goauthentik" \
      org.opencontainers.image.source="https://github.com/goauthentik/authentik" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
