# =============================================================================
# EVERGREEN HARDENED YARN
# Generated from template - Version: 1.22.22
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.22.22
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm ca-certificates curl && rm -rf /var/lib/apt/lists/* && \
    npm install -g yarn --omit=dev 2>/dev/null && \
    useradd -m -u 65532 -s /usr/bin/false app 2>/dev/null || true && \
    mkdir -p /app /var/log/node /var/cache/node 2>/dev/null || true


ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim

RUN apk add --no-cache nodejs-20 ca-certificates curl
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/node /var/log/node
COPY --from=builder --chown=65532:65532 /var/cache/node /var/cache/node
USER 65532:65532
WORKDIR /app
EXPOSE 0

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:0/ || exit 1
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "node"]
LABEL org.opencontainers.image.title="yarn" \
      org.opencontainers.image.description="yarn container image" \
      org.opencontainers.image.version="1.22.22" \
      org.opencontainers.image.vendor="Yarn" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
            org.opencontainers.image.source="https://github.com/yarnpkg/yarn"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
