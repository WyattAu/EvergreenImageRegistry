# =============================================================================
# SOVEREIGN HARDENED SONARR-DEVELOP
# Generated from template - Version: 4.0.11
# Constraint: debian-slim - .NET runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.0.11
ARG BUILD_DATE


FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Sonarr/Sonarr/releases/download/v4.0.11/Sonarr.develop.4.0.11.linux-core-x64.tar.gz -o /Sonarr.tar.gz && \
    [ -f /Sonarr.tar.gz ] && tar -xzf /Sonarr.tar.gz -C /app && rm /Sonarr.tar.gz && chmod +x /app/Sonarr 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Sonarr/Sonarr/releases/download/v4.0.11/Sonarr.develop.4.0.11.linux-core-x64.tar.gz -o /app/Sonarr && chmod +x /app/Sonarr || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl || true
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/sonarr-develop /var/cache/sonarr-develop && chown -R 65532:65532 /var/log/sonarr-develop /var/cache/sonarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8989
ENTRYPOINT ["/app/Sonarr"]
LABEL org.opencontainers.image.title="sonarr-develop" \
      org.opencontainers.image.version="4.0.11" \
      org.opencontainers.image.vendor="Sonarr" \
      org.opencontainers.image.source="https://github.com/Sonarr/Sonarr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM