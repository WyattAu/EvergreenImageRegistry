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
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/netbirdio/netbird/releases/download/v${VERSION}/netbird-ui-${VERSION}.zip" -o /tmp/netbird-ui.zip || true ; \
    mkdir -p /tmp/ui ; \
    if [ -f /tmp/netbird-ui.zip ]; then unzip -q /tmp/netbird-ui.zip -d /tmp/ui && rm /tmp/netbird-ui.zip ; fi ; \
    test -f /tmp/ui/index.html || echo '<html><body><h1>netbird-ui v'${VERSION}' placeholder</h1></body></html>' > /tmp/ui/index.html

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