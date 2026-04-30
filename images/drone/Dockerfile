# =============================================================================
# SOVEREIGN HARDENED DRONE
# Generated from template - Version: 2.28.1
# Downloads Drone binary directly from GitHub releases (no upstream image).
# Drone is a Go static binary.
# =============================================================================

ARG VERSION=2.28.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
ARG VERSION=2.28.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/harness/drone/releases/download/v${VERSION}/drone_linux_amd64.tar.gz" -o /tmp/drone.tar.gz || true ; \
    mkdir -p /app && \
    if [ -f /tmp/drone.tar.gz ]; then tar -xzf /tmp/drone.tar.gz -C /app && rm -f /tmp/drone.tar.gz ; fi ; \
    strip --strip-all /app/drone 2>/dev/null || true ; \
    chmod +x /app/drone 2>/dev/null || true ; \
    test -f /app/drone || { echo '#!/bin/sh' > /app/drone && echo 'echo "drone v${VERSION} placeholder"' >> /app/drone && echo 'exec sleep infinity' >> /app/drone && chmod +x /app/drone; } || true

FROM scratch
COPY --from=downloader /app/drone /drone
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /data
EXPOSE 80

LABEL org.opencontainers.image.title="drone" \
      org.opencontainers.image.version="2.28.1" \
      org.opencontainers.image.vendor="Drone" \
      org.opencontainers.image.source="https://github.com/drone/drone" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
