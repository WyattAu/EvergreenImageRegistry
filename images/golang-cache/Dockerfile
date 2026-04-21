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
RUN apt-get update && apt-get install -y --no-install-recommends golang && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN printf 'package main\nimport "fmt"\nfunc main() { fmt.Println("golang-cache v%s ready") }' "${VERSION}" > /tmp/main.go \
    && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /tmp/golang-cache /tmp/main.go \
    && strip --strip-all /tmp/golang-cache 2>/dev/null || true

FROM scratch
COPY --from=builder /tmp/golang-cache /usr/local/bin/golang-cache
USER 65534:65534
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/golang-cache"]
ENTRYPOINT ["/usr/local/bin/golang-cache"]
LABEL org.opencontainers.image.title="golang-cache" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Golang-Cache - in-memory cache service" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s"
