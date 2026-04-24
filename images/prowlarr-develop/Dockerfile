# =============================================================================
# SOVEREIGN HARDENED PROWLARR-DEVELOP
# Generated from template - Version: 1.29.0
# Constraint: debian-slim - .NET runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.29.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Prowlarr/Prowlarr/releases/download/v1.29.0/Prowlarr.develop.1.29.0.linux-core-x64.tar.gz" -o /Prowlarr.tar.gz && \
    tar -xzf /Prowlarr.tar.gz -C /app && rm /Prowlarr.tar.gz && chmod +x /app/Prowlarr 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/Prowlarr/Prowlarr/releases/download/v1.29.0/Prowlarr.develop.1.29.0.linux-core-x64.tar.gz" -o /app/Prowlarr && chmod +x /app/Prowlarr


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/prowlarr-develop /var/cache/prowlarr-develop && chown -R 65532:65532 /var/log/prowlarr-develop /var/cache/prowlarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9696
ENTRYPOINT ["/app/Prowlarr"]
LABEL org.opencontainers.image.title="prowlarr-develop" \
      org.opencontainers.image.version="1.29.0" \
      org.opencontainers.image.vendor="Prowlarr" \
      org.opencontainers.image.source="https://github.com/Prowlarr/Prowlarr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM