# =============================================================================
# SOVEREIGN HARDENED BSONDB
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: PLACEHOLDER - no upstream static binary available
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates || true
RUN adduser -u 65532 -s /sbin/nologin bsondb 2>/dev/null || true
RUN mkdir -p /var/lib/bsondb /var/log/bsondb /var/cache/bsondb /app 2>/dev/null || true
RUN chown -R 65532:65532 /var/lib/bsondb /var/log/bsondb /var/cache/bsondb /app
USER 65532:65532
WORKDIR /app
EXPOSE 27017
ENTRYPOINT ["/app/bsondb"]
LABEL org.opencontainers.image.title="bsondb" \
      org.opencontainers.image.version="${VERSION}" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM