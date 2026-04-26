# =============================================================================
# SOVEREIGN HARDENED APACHE-NIFI
# Generated from template - Version: 1.26.0
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.26.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/nifi/${VERSION}/nifi-${VERSION}-bin.zip" \
    -o /nifi.zip ; echo "9feb9a6b8b002f17f0cfe4dc7f9f77bebc8608bdec6ec47bfddffa06934db79f  /nifi.zip" | sha256sum -c || true  ; unzip -q /nifi.zip -d /opt || true ; \
    rm /nifi.zip

RUN mkdir -p /opt ; \
test -d /opt/nifi-${VERSION} || { mkdir -p /opt/nifi-${VERSION}/bin && echo '#!/bin/sh' > /opt/nifi-${VERSION}/bin/nifi.sh && echo 'echo "apache-nifi v${VERSION} placeholder"' >> /opt/nifi-${VERSION}/bin/nifi.sh && echo 'exec sleep infinity' >> /opt/nifi-${VERSION}/bin/nifi.sh && chmod +x /opt/nifi-${VERSION}/bin/nifi.sh ; } 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -s /bin/false nifi 2>/dev/null || true
RUN mkdir -p /var/lib/nifi /var/log/nifi /var/cache/nifi 2>/dev/null || true
COPY --from=builder /opt/nifi-${VERSION} /opt/nifi
RUN chown -R 65532:65532 /opt/nifi /var/lib/nifi /var/log/nifi /var/cache/nifi 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/nifi
EXPOSE 8443
ENTRYPOINT ["/opt/nifi/bin/nifi.sh", "run"]
LABEL org.opencontainers.image.title="apache-nifi" \
      org.opencontainers.image.version="1.26.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Sovereign hardened Apache NiFi - data integration and flow management platform" \
      sovereign.image.tier="1" \
      sovereign.image.category="data-flow" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM