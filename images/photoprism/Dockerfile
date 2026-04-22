# =============================================================================
# SOVEREIGN HARDENED PHOTOPRISM
# Generated from template - Version: 240427
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=240427
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://dl.photoprism.app/pkg/linux-amd64/photoprism-${VERSION}-linux-amd64.tar.gz" -o /tmp/photoprism.tar.gz && \
    tar -xzf /tmp/photoprism.tar.gz -C /opt && rm /tmp/photoprism.tar.gz && \
    chmod +x /opt/photoprism 2>/dev/null || true
RUN useradd -m -u 65532 -g '' photoprism 2>/dev/null || true
RUN mkdir -p /app /var/log/photoprism /var/cache/photoprism && chown -R photoprism:photoprism /app /var/log/photoprism /var/cache/photoprism /opt/photoprism 2>/dev/null || true
USER photoprism
WORKDIR /app
EXPOSE 2282
ENTRYPOINT ["/opt/photoprism"]
LABEL org.opencontainers.image.title="photoprism" \
      org.opencontainers.image.version="240427" \
      org.opencontainers.image.vendor="PhotoPrism" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM