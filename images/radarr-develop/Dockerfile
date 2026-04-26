# =============================================================================
# SOVEREIGN HARDENED RADARR-DEVELOP
# Generated from template - Version: 5.15.0
# Constraint: debian-slim - .NET runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.15.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Radarr/Radarr/releases/download/v5.15.0/Radarr.develop.5.15.0.linux-core-x64.tar.gz -o /Radarr.tar.gz && \
    [ -f /Radarr.tar.gz ] && tar -xzf /Radarr.tar.gz -C /app && rm /Radarr.tar.gz && chmod +x /app/Radarr 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Radarr/Radarr/releases/download/v5.15.0/Radarr.develop.5.15.0.linux-core-x64.tar.gz -o /app/Radarr && chmod +x /app/Radarr || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/radarr-develop /var/cache/radarr-develop && chown -R 65532:65532 /var/log/radarr-develop /var/cache/radarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 7878
ENTRYPOINT ["/app/Radarr"]
LABEL org.opencontainers.image.title="radarr-develop" \
      org.opencontainers.image.version="5.15.0" \
      org.opencontainers.image.vendor="Radarr" \
      org.opencontainers.image.source="https://github.com/Radarr/Radarr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM