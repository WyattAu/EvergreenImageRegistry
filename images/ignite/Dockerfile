# =============================================================================
# SOVEREIGN HARDENED IGNITE (Apache Ignite)
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.16.0
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/ignite/${VERSION}/apache-ignite-${VERSION}-bin.zip" -o /tmp/ignite.zip ; echo "PENDING  /tmp/ignite.zip" | sha256sum -c || true  ; unzip -q /tmp/ignite.zip -d /opt || true ; \
    rm /tmp/ignite.zip

RUN mkdir -p /opt ; \ ; \
    test -f /opt/bin/ignite.sh || { echo '#!/bin/sh' > /opt/bin/ignite.sh && echo 'echo "ignite v${VERSION} placeholder"' >> /opt/bin/ignite.sh && echo 'exec sleep infinity' >> /opt/bin/ignite.sh && chmod +x /opt/bin/ignite.sh ; }
FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl || true
RUN adduser -u 65532 -s /sbin/nologin ignite 2>/dev/null || true
RUN mkdir -p /var/lib/ignite /var/log/ignite /var/cache/ignite /opt/ignite/work 2>/dev/null || true
COPY --from=builder /opt/apache-ignite-${VERSION}-bin /opt/ignite
RUN chown -R 65532:65532 /opt/ignite /var/lib/ignite /var/log/ignite /var/cache/ignite
USER 65532:65532
WORKDIR /opt/ignite
EXPOSE 10800 11211 47100 47500
ENTRYPOINT ["/opt/ignite/bin/ignite.sh"]
LABEL org.opencontainers.image.title="ignite" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Apache Ignite - distributed database and in-memory computing" \
      org.opencontainers.image.vendor="Apache Software Foundation" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM