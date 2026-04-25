# =============================================================================
# SOVEREIGN HARDENED PERKUNADB
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: PLACEHOLDER - no upstream static binary available
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates || true
RUN adduser -u 65532 -s /sbin/nologin perkunadb 2>/dev/null || true
RUN mkdir -p /var/lib/perkunadb /var/log/perkunadb /var/cache/perkunadb /app 2>/dev/null || true
RUN chown -R 65532:65532 /var/lib/perkunadb /var/log/perkunadb /var/cache/perkunadb /app
USER 65532:65532
WORKDIR /app
EXPOSE 5432
ENTRYPOINT ["/app/perkunadb"]
LABEL org.opencontainers.image.title="perkunadb" \
      org.opencontainers.image.version="${VERSION}" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM