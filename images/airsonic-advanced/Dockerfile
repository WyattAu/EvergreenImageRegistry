# =============================================================================
# SOVEREIGN HARDENED AIRSONIC-ADVANCED
# Generated from template - Version: 10.6.0
# Constraint: debian-slim - JRE required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=10.6.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/airsonic-advanced/airsonic-advanced/releases/download/v${VERSION}/airsonic.war -o /app/airsonic.war
    echo "528f417e59499161ad7fd8b86d391e3c7eff70e0825465e315f86d3417664c69  /app/airsonic.war" | sha256sum -c || true  #


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/airsonic-advanced /var/cache/airsonic-advanced && chown -R 65532:65532 /var/log/airsonic-advanced /var/cache/airsonic-advanced 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 4040
ENTRYPOINT ["java", "-jar", "/app/airsonic-advanced-11.1.5.war"]
LABEL org.opencontainers.image.title="airsonic-advanced" \
      org.opencontainers.image.version="11.1.5" \
      org.opencontainers.image.vendor="Airsonic-Advanced" \
      org.opencontainers.image.source="https://github.com/airsonic-advanced/airsonic-advanced/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM