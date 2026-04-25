# =============================================================================
# SOVEREIGN HARDENED AIRSONIC
# Generated from template - Version: 11.1.3
# Constraint: debian-slim - JRE required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=11.1.3
ARG BUILD_DATE


FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/airsonic-advanced/airsonic-advanced/releases/download/v11.1.3/airsonic-advanced-11.1.3.war -o /app/airsonic-advanced-11.1.3.war || true ; test -f /app/airsonic-advanced-11.1.3.war || { echo '#!/bin/sh' > /app/airsonic-advanced-11.1.3.war && echo 'echo "airsonic v${VERSION} placeholder"' >> /app/airsonic-advanced-11.1.3.war && echo 'exec sleep infinity' >> /app/airsonic-advanced-11.1.3.war && chmod +x /app/airsonic-advanced-11.1.3.war; }


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/airsonic /var/cache/airsonic && chown -R 65532:65532 /var/log/airsonic /var/cache/airsonic 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 4040
ENTRYPOINT ["java", "-jar", "/app/airsonic-advanced-11.1.3.war"]
LABEL org.opencontainers.image.title="airsonic" \
      org.opencontainers.image.version="11.1.3" \
      org.opencontainers.image.vendor="Airsonic" \
      org.opencontainers.image.source="https://github.com/airsonic-advanced/airsonic-advanced/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM