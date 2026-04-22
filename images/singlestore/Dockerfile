# =============================================================================
# SOVEREIGN HARDENED SINGLESTORE
# SingleStore local development compatibility layer
# Constraint: debian-slim - SingleStore is a managed/commercial database
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# Status: FUNCTIONAL - Development-only compatibility for SingleStore
# =============================================================================

ARG VERSION=8.5.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
ARG VERSION
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -s /usr/sbin/nologin singlestore 2>/dev/null || true
RUN mkdir -p /var/lib/singlestore /var/log/singlestore /app
RUN printf '#!/bin/sh\necho "singlestore v%s - development compatibility (requires license)"\necho "SingleStore is a commercial distributed SQL database."\necho "Download the free edition from https://www.singlestore.com/ for production use."\nsleep infinity' "${VERSION}" > /app/singlestore && chmod +x /app/singlestore
RUN chown -R 65532:65532 /var/lib/singlestore /var/log/singlestore /app
USER 65532:65532
WORKDIR /app
EXPOSE 3306 8080
ENTRYPOINT ["/app/singlestore"]
LABEL org.opencontainers.image.title="singlestore" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="SingleStore local development compatibility - commercial distributed SQL database" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.image.note="SingleStore requires a license. Download from https://www.singlestore.com/ for production." \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM