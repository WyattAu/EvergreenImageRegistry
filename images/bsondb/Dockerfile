# =============================================================================
# SOVEREIGN HARDENED BSONDB
# Constraint: debian-slim - niche database, placeholder binary
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: PLACEHOLDER - no upstream static binary available
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -s /usr/sbin/nologin bsondb 2>/dev/null || true
RUN mkdir -p /var/lib/bsondb /var/log/bsondb /var/cache/bsondb /app
RUN printf '#!/bin/sh\necho "bsondb v%s - placeholder (no upstream binary)"\nsleep infinity' "${VERSION}" > /app/bsondb && chmod +x /app/bsondb
RUN chown -R 65532:65532 /var/lib/bsondb /var/log/bsondb /var/cache/bsondb /app
USER 65532:65532
WORKDIR /app
EXPOSE 27017
ENTRYPOINT ["/app/bsondb"]
LABEL org.opencontainers.image.title="bsondb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened BSONDB - BSON document database (placeholder)" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="placeholder" \
      sovereign.image.note="No upstream binary available. Replace placeholder when upstream publishes releases." \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM