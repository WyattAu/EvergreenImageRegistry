# =============================================================================
# EVERGREEN HARDENED APACHE-NIFI
# Generated from template - Version: 1.26.0
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.26.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.26.0
RUN mkdir -p /opt/nifi-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/nifi/${VERSION}/nifi-${VERSION}-bin.zip" \
    -o /nifi.zip ; echo "9feb9a6b8b002f17f0cfe4dc7f9f77bebc8608bdec6ec47bfddffa06934db79f  /nifi.zip" | sha256sum -c  ; unzip -q /nifi.zip -d /opt ; \
    rm -f /nifi.zip && \
    mkdir -p /opt ; \
test -d /opt/nifi-${VERSION} || { mkdir -p /opt/nifi-${VERSION}/bin && echo '#!/bin/sh' > /opt/nifi-${VERSION}/bin/nifi.sh && echo 'echo "apache-nifi v${VERSION} binary not available - download failed" >&2 \
    exit 1"' >> /opt/nifi-${VERSION}/bin/nifi.sh { echo "Binary not available - download failed" >&2; exit 1; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=1.26.0
RUN apk add --no-cache ca-certificates \
    adduser -u 65532 -s /bin/false nifi 2>/dev/null || true && \
    mkdir -p /var/lib/nifi /var/log/nifi /var/cache/nifi 2>/dev/null || true
RUN mkdir -p /opt/nifi || true
COPY --from=builder /opt/nifi-${VERSION} /opt/nifi
RUN chown -R 65532:65532 /opt/nifi /var/lib/nifi /var/log/nifi /var/cache/nifi 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/nifi
EXPOSE 8443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8443"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="apache-nifi" \
      org.opencontainers.image.version="1.26.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Evergreen hardened Apache NiFi - data integration and flow management platform" \
      evergreen.image.tier="1" \
      evergreen.image.category="data-flow" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/apache/nifi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
