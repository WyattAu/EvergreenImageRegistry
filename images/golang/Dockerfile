# =============================================================================
# EVERGREEN HARDENED GOLANG
# Generated from template - Version: 1.22.3
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.22.3
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    go-1.23-go ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    useradd -m -u 65532 -s /usr/bin/false go 2>/dev/null || true && \
    mkdir -p /app /var/log/go /var/cache/go
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/go /var/log/go
COPY --from=builder --chown=65532:65532 /var/cache/go /var/cache/go
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["go"]
LABEL org.opencontainers.image.title="go-1.23" \
      org.opencontainers.image.description="golang container image" \
      org.opencontainers.image.version="1.22.3" \
      org.opencontainers.image.vendor="Go" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
            org.opencontainers.image.source="https://github.com/golang/go"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
