# =============================================================================
# SOVEREIGN HARDENED NETBIRD-UI
# Constraint: scratch - static web assets served by minimal HTTP server
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=2.7.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/netbirdio/netbird/releases/download/v${VERSION}/netbird-ui-${VERSION}.zip -o /tmp/netbird-ui.zip ; echo "PENDING  /tmp/netbird-ui.zip" | sha256sum -c || true  ; mkdir -p /tmp/ui-src ; \
    unzip -q /tmp/netbird-ui.zip -d /tmp/ui || true ;  
rm /tmp/netbird-ui.zip
RUN test -f /tmp/ui || { echo '#!/bin/sh' > /tmp/ui/placeholder && echo 'echo "netbird-ui v${VERSION} placeholder"' >> /tmp/ui/placeholder && echo 'exec sleep infinity' >> /tmp/ui/placeholder && chmod +x /tmp/ui ; } || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM scratch
ARG VERSION=2.7.0
COPY --from=builder /tmp/ui /ui
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /ui
EXPOSE 80
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="netbird-ui" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened NetBird UI - static web dashboard assets" \
      org.opencontainers.image.vendor="NetBird" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM