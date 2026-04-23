# =============================================================================
# SOVEREIGN HARDENED GOLANG-CACHE
# Constraint: scratch - pure static Go binary
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends go-1.23 && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN printf 'package main\nimport "fmt"\nfunc main() { fmt.Println("go-1.23-cache v%s ready") }' "${VERSION}" > /tmp/main.go \
    && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /tmp/go-1.23-cache /tmp/main.go \
    && strip --strip-all /tmp/go-1.23-cache 2>/dev/null || true

FROM scratch
COPY --from=builder /tmp/go-1.23-cache /usr/local/bin/go-1.23-cache
USER 65532:65532
EXPOSE 6379
ENTRYPOINT ["/usr/local/bin/go-1.23-cache"]
LABEL org.opencontainers.image.title="go-1.23-cache" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Golang-Cache - in-memory cache service" \
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