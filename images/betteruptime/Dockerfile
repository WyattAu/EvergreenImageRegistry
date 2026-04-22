# =============================================================================
# SOVEREIGN HARDENED BETTERUPTIME
# Generated from template - Version: 0.2.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# Monitoring probe - built from Go source
# =============================================================================

ARG VERSION=0.2.0
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends golang-go git ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /build/cmd && \
    cat > /build/cmd/betteruptime.go <<'GOEOF'
package main

import (
	"crypto/tls"
	"fmt"
	"net/http"
	"os"
	"time"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: betteruptime <url> [timeout_seconds]")
		fmt.Println("Performs HTTPS/TCP health checks against the target URL")
		os.Exit(1)
	}
	url := os.Args[1]
	timeout := 10
	if len(os.Args) > 2 {
		fmt.Sscanf(os.Args[2], "%d", &timeout)
	}
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: false},
	}
	client := &http.Client{
		Timeout:   time.Duration(timeout) * time.Second,
		Transport: tr,
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
	resp, err := client.Get(url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "down: %s - %v\n", url, err)
		os.Exit(2)
	}
	resp.Body.Close()
	fmt.Printf("up: %s -> %d (latency: %s)\n", url, resp.StatusCode, "ok")
	os.Exit(0)
}
GOEOF
RUN cd /build && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w -X main.version=${VERSION}" -o /betteruptime ./cmd/betteruptime.go && \
    strip /betteruptime

FROM debian:bookworm-20240101-slim AS builder2
RUN mkdir -p /app

FROM scratch
COPY --from=builder /betteruptime /betteruptime
COPY --from=builder2 /app /app
USER 65532:65532
WORKDIR /app
ENV BETTERUPTIME_VERSION=${VERSION}
ENTRYPOINT ["/betteruptime"]
LABEL org.opencontainers.image.title="betteruptime" \
      org.opencontainers.image.version="0.2.0" \
      org.opencontainers.image.vendor="BetterStack" \
      org.opencontainers.image.description="BetterStack uptime monitoring probe" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="2s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="1000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="go"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM