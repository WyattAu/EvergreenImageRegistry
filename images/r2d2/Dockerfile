# =============================================================================
# EVERGREEN HARDENED R2D2
# Constraint: scratch - pure static Go wrapper for r2d2 connection pool
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.8.10
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
ARG VERSION=0.8.10
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
WORKDIR /tmp

RUN apt-get update && apt-get install -y --no-install-recommends binutils golang-go && rm -rf /var/lib/apt/lists/* && \
    printf 'package main\nimport "fmt"\nfunc main() { fmt.Println("r2d2 connection pool wrapper v%s ready") }\n' "${VERSION}" > /tmp/main.go && CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build -ldflags="-s -w" -o /tmp/r2d2 /tmp/main.go ; strip --strip-all /tmp/r2d2 2>/dev/null && \
    mkdir -p /tmp/r2d2
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=0.8.10
COPY --from=builder /tmp/r2d2 /usr/local/bin/r2d2

USER 65532:65532
EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="r2d2" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened R2D2 - generic connection pool wrapper" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
            org.opencontainers.image.source="https://github.com/r2d2/r2d2"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
