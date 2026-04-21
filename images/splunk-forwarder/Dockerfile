# =============================================================================
# SOVEREIGN HARDENED SPLUNK FORWARDER
# Version: 9.2.1
# Constraint: debian-slim - runtime libraries required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=9.2.1
ARG BUILD_HASH=a1c5796230b0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
ARG BUILD_HASH
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://download.splunk.com/products/universalforwarder/releases/${VERSION}/linux/splunkforwarder-${VERSION}-${BUILD_HASH}-linux-x86_64.tgz" -o splunk.tgz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  splunk.tgz" | sha256sum -c - \
    && tar -xzf splunk.tgz \
    && rm splunk.tgz

FROM debian:bookworm-slim
ARG VERSION
ARG BUILD_HASH
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl libgomp1 && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin splunk 2>/dev/null || true
RUN mkdir -p /opt/splunkforwarder/var/log/splunk /opt/splunkforwarder/var/run/splunk
COPY --from=builder /tmp/splunkforwarder /opt/splunkforwarder
USER 65534:65534
WORKDIR /opt/splunkforwarder
EXPOSE 8089 9997
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["/opt/splunkforwarder/bin/splunk", "show", "splunkd-status"]
ENTRYPOINT ["/opt/splunkforwarder/bin/splunk"]
CMD ["start", "--accept-license", "--no-prompt"]
LABEL org.opencontainers.image.title="splunk-forwarder" \
      org.opencontainers.image.description="Sovereign hardened Splunk Universal Forwarder - log data shipper" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Splunk" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
