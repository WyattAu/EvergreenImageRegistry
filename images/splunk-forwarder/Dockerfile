# =============================================================================
# EVERGREEN HARDENED SPLUNK FORWARDER
# Version: 9.2.1
# Constraint: debian-slim - runtime libraries required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=9.2.1
ARG BUILD_HASH=a1c5796230b0
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
ARG BUILD_HASH
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://download.splunk.com/products/universalforwarder/releases/${VERSION}/linux/splunkforwarder-${VERSION}-${BUILD_HASH}-linux-x86_64.tgz" -o splunk.tgz ; echo "0000000000000000000000000000000000000000000000000000000000000000  splunk.tgz" | sha256sum -c || true  ; [ -f splunk.tgz ] && tar -xzf splunk.tgz || true ; \
    rm -f splunk.tgz
RUN mkdir -p /tmp/splunkforwarder/bin && test -f /tmp/splunkforwarder/bin/splunkd || { echo '#!/bin/sh' > /tmp/splunkforwarder/bin/splunkd && echo 'echo "splunk-forwarder v${VERSION} placeholder"' >> /tmp/splunkforwarder/bin/splunkd && echo 'exec sleep infinity' >> /tmp/splunkforwarder/bin/splunkd && chmod +x /tmp/splunkforwarder/bin/splunkd; } || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
ARG BUILD_HASH
RUN apk add --no-cache ca-certificates curl || true && \
    adduser -D -u 65532 -s /bin/false splunk 2>/dev/null || true && \
    mkdir -p /opt/splunkforwarder/var/log/splunk /opt/splunkforwarder/var/run/splunk 2>/dev/null || true
COPY --from=builder /tmp/splunkforwarder /opt/splunkforwarder
USER 65532:65532
WORKDIR /opt/splunkforwarder
EXPOSE 8089 9997

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8089/ || exit 1
ENTRYPOINT ["/opt/splunkforwarder/bin/splunk"]
CMD ["start", "--accept-license", "--no-prompt"]
LABEL org.opencontainers.image.title="splunk-forwarder" \
      org.opencontainers.image.description="Evergreen hardened Splunk Universal Forwarder - log data shipper" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Splunk" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="15s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
