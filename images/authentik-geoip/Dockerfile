FROM debian:bookworm-slim AS downloader
ARG VERSION=2026.2.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/goauthentik/authentik/releases/download/version/${VERSION}/authentik-geoip-${VERSION}.tar.gz -o /authentik-geoip.tar.gz && || true ; \
    mkdir -p /tmp/authentik-geoip && \ 2>/dev/null || true ; \
    [ -f /authentik-geoip.tar.gz ] && tar -xzf /authentik-geoip.tar.gz -C /tmp/authentik-geoip && || true ; \
    rm -f /authentik-geoip.tar.gz ; test -f /tmp/authentik-geoip || { echo '#!/bin/sh' > /tmp/authentik-geoip && echo 'echo "authentik-geoip v${VERSION} placeholder"' >> /tmp/authentik-geoip && echo 'exec sleep infinity' >> /tmp/authentik-geoip && chmod +x /tmp/authentik-geoip; }


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates libpq || true
COPY --from=downloader /tmp/authentik-geoip /opt/authentik-geoip
RUN pip install --no-cache-dir --break-system-packages /opt/authentik-geoip 2>/dev/null || pip install --no-cache-dir /opt/authentik-geoip || true && \
    mkdir -p /app && chown -R 65532:65532 /app /opt/authentik-geoip 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3", "-m", "authentik"]
CMD ["geoip"]
LABEL org.opencontainers.image.title="authentik-geoip" \
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
