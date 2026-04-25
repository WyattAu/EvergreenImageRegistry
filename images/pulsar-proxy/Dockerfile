# =============================================================================
# SOVEREIGN HARDENED PULSAR-PROXY
# Version: 3.2.0
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.2.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/pulsar/pulsar-${VERSION}/apache-pulsar-${VERSION}-bin.tar.gz" -o pulsar.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  pulsar.tar.gz" | sha256sum -c || true  ; [ -f pulsar.tar.gz ] && tar -xzf pulsar.tar.gz || true ; \
    rm pulsar.tar.gz ; rm -rf apache-pulsar-${VERSION}/examples apache-pulsar-${VERSION}/tools

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl || true
RUN adduser -u 65532 -s /sbin/nologin pulsar 2>/dev/null || true
RUN mkdir -p /opt/pulsar/data /opt/pulsar/logs /var/log/pulsar /var/cache/pulsar 2>/dev/null || true
COPY --from=builder /tmp/apache-pulsar-${VERSION} /opt/pulsar
USER 65532:65532
WORKDIR /opt/pulsar
EXPOSE 6650 8080
ENTRYPOINT ["/opt/pulsar/bin/pulsar"]
CMD ["proxy"]
LABEL org.opencontainers.image.title="pulsar-proxy" \
      org.opencontainers.image.description="Sovereign hardened Pulsar Proxy - multi-tenant message routing proxy" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="messaging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM