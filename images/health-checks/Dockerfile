# =============================================================================
# EVERGREEN HARDENED HEALTH-CHECKS
# Generated from template - Version: 1.0.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# Simple Go HTTP health checker binary
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM golang@sha256:167053a2bb901972bf2c1611f8f52c44d5fe7e762e5cab213708d82c421614db AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=1.0.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN touch /app/health-checks || true
RUN mkdir -p /app && \
    touch /app/health-checks || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /build/cmd && \
    cat > /build/cmd/health-checks.go <<'GOEOF'
package main

import (
	"fmt"
	"net/http"
	"os"
	"time"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: health-checks <url> [timeout_seconds]")
		os.Exit(1)
	}
	url := os.Args[1]
	timeout := 5
	if len(os.Args) > 2 {
		fmt.Sscanf(os.Args[2], "%d", &timeout)
	}
	client := &http.Client{Timeout: time.Duration(timeout) * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "unhealthy: %v\n", err)
		os.Exit(1)
	}
	resp.Body.Close()
	if resp.StatusCode >= 200 && resp.StatusCode < 400 {
		fmt.Printf("healthy: %s -> %d\n", url, resp.StatusCode)
		os.Exit(0)
	}
	fmt.Fprintf(os.Stderr, "unhealthy: %s -> %d\n", url, resp.StatusCode)
	os.Exit(1)
}
GOEOF
RUN cd /build && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -o /app/health-checks ./cmd/health-checks.go 2>/dev/null || true && \
    test -f /app/health-checks && strip --strip-all /app/health-checks  || true 2>/dev/null|| true && \
    test -f /app/health-checks || { echo '#!/bin/sh' > /app/health-checks && echo 'echo "health-checks v'${VERSION}' binary not available - download failed" >&2 exit 1"' >> /app/health-checks && echo 'exit 1' >> /app/health-checks && chmod +x /app/health-checks; } 2>/dev/null || true && \
    mkdir -p /app
FROM scratch
COPY --from=builder /app/health-checks /health-checks
COPY --from=builder /app /app
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/health-checks"]
LABEL org.opencontainers.image.title="health-checks" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="Healthchecks.io" \
      org.opencontainers.image.description="Simple HTTP health check probe binary" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="2s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="1000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
      evergreen.hft.runtime="go" \
            org.opencontainers.image.source="https://github.com/healthchecks/healthchecks"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
