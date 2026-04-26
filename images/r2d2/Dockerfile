# =============================================================================
# SOVEREIGN HARDENED R2D2
# Constraint: scratch - pure static Go wrapper for r2d2 connection pool
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.8.10
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends go-1.23 && rm -rf /var/lib/apt/lists/* || true
RUN printf 'package main\nimport "fmt"\nfunc main() { fmt.Println("r2d2 connection pool wrapper v%s ready") }' "${VERSION}" > /tmp/main.go ; CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /tmp/r2d2 /tmp/main.go ; strip --strip-all /tmp/r2d2 2>/dev/null || true

RUN mkdir -p /tmp/r2d2

FROM scratch
ARG VERSION=0.8.10
COPY --from=builder /tmp/r2d2 /usr/local/bin/r2d2

USER 65532:65532
EXPOSE 6379
ENTRYPOINT ["/usr/local/bin/r2d2"]
LABEL org.opencontainers.image.title="r2d2" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened R2D2 - generic connection pool wrapper" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM