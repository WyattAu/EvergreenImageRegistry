# =============================================================================
# SOVEREIGN HARDENED SUBSONIC
# Generated from template - Version: 6.17.1
# Constraint: debian-slim - JRE required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=6.17.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/subsonic/subsonic/releases/download/v6.17.1/subsonic-6.17.1.jar" -o /app/subsonic-6.17.1.jar

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates curl
RUN useradd -m -u 65532 -g '' app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/subsonic /var/cache/subsonic && chown -R 65532:65532 /var/log/subsonic /var/cache/subsonic 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 4040
ENTRYPOINT ["java", "-jar", "/app/subsonic-6.17.1.jar"]
LABEL org.opencontainers.image.title="subsonic" \
      org.opencontainers.image.version="6.17.1" \
      org.opencontainers.image.vendor="Subsonic" \
      org.opencontainers.image.source="https://github.com/subsonic/subsonic/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM