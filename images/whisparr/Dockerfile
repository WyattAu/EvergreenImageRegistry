# =============================================================================
# SOVEREIGN HARDENED WHISPARR
# Generated from template - Version: 1.0.0.329
# Constraint: debian-slim - .NET runtime required
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.0.0.329
ARG BUILD_DATE


FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Whisparr/Whisparr/releases/download/v1.0.0.329/Whisparr.develop.1.0.0.329.linux-core-x64.tar.gz" -o /Whisparr.tar.gz && \
    tar -xzf /Whisparr.tar.gz -C /app && rm /Whisparr.tar.gz && chmod +x /app/Whisparr 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Whisparr/Whisparr/releases/download/v1.0.0.329/Whisparr.develop.1.0.0.329.linux-core-x64.tar.gz" -o /app/Whisparr && chmod +x /app/Whisparr


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/whisparr /var/cache/whisparr && chown -R 65532:65532 /var/log/whisparr /var/cache/whisparr 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6969
ENTRYPOINT ["/app/Whisparr"]
LABEL org.opencontainers.image.title="whisparr" \
      org.opencontainers.image.version="1.0.0.329" \
      org.opencontainers.image.vendor="Whisparr" \
      org.opencontainers.image.source="https://github.com/Whisparr/Whisparr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM