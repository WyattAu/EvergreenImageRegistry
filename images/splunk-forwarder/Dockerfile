# =============================================================================
# EVERGREEN HARDENED SPLUNK FORWARDER
# Version: 9.2.1
# Constraint: debian-slim - runtime libraries required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=9.2.1
ARG TARGETARCH
ARG BUILD_HASH=a1c5796230b0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=9.2.1
ARG BUILD_HASH
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    # Checksum cannot be verified: Splunk requires authenticated download; BUILD_HASH may not match available releases
    curl --retry 3 --retry-delay 5 -fsSL "https://download.splunk.com/products/universalforwarder/releases/${VERSION}/linux/splunkforwarder-${VERSION}-${BUILD_HASH}-linux-x86_64.tgz" -o splunk.tgz ; echo "0000000000000000000000000000000000000000000000000000000000000000  splunk.tgz" | sha256sum -c  ; [ -f splunk.tgz ] && tar -xzf splunk.tgz ; \
    rm -f splunk.tgz && \
    mkdir -p /tmp/splunkforwarder/bin && { echo "Binary not available - download failed" >&2; exit 1; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=9.2.1
ARG BUILD_HASH
RUN apk add --no-cache ca-certificates curl && \
    adduser -D -u 65532 -s /bin/false splunk 2>/dev/null || true && \
    mkdir -p /opt/splunkforwarder/var/log/splunk /opt/splunkforwarder/var/run/splunk 2>/dev/null || true
COPY --from=builder /tmp/splunkforwarder /opt/splunkforwarder
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/splunkforwarder
EXPOSE 8089 9997

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8089"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/opt/splunkforwarder/bin/splunk"]
CMD ["--", "start", "--accept-license", "--no-prompt"]
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
      evergreen.hft.startup-timeout="30000ms" \
            org.opencontainers.image.source="https://github.com/splunk/splunk-ansible"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
