# =============================================================================
# SOVEREIGN HARDENED BUDIBASE-WORKER
# Generated from template - Version: 2.14.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.14.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm ca-certificates curl && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 65532 -s /usr/sbin/nologin app 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache nodejs ca-certificates curl
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/node /var/log/node
COPY --from=builder --chown=65532:65532 /var/cache/node /var/cache/node
USER 65532:65532
WORKDIR /app
EXPOSE 10001
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="budibase-worker" \
      org.opencontainers.image.version="2.14.0" \
      org.opencontainers.image.vendor="Budibase/budibase" \
      org.opencontainers.image.source="https://github.com/Budibase/budibase/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM