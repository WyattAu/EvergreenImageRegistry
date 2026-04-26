# =============================================================================
# SOVEREIGN HARDENED VULCAN
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: PLACEHOLDER - no upstream static binary available
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -s /bin/false vulcan 2>/dev/null || true
RUN mkdir -p /var/lib/vulcan /var/log/vulcan /var/cache/vulcan /app 2>/dev/null || true
RUN chown -R 65532:65532 /var/lib/vulcan /var/log/vulcan /var/cache/vulcan /app
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/app/vulcan"]
LABEL org.opencontainers.image.title="vulcan" \
      org.opencontainers.image.version="${VERSION}" \
      sovereign.image.tier="1" \
      sovereign.image.category="tooling" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM