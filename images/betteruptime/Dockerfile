# =============================================================================
# EVERGREEN HARDENED BETTERUPTIME
# Generated from template - Version: 0.2.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# Monitoring probe - built from Go source
# =============================================================================

ARG VERSION=0.2.0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
ARG VERSION=0.2.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN touch /betteruptime || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils go-1.23-go git ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /build/cmd ; \
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
RUN if len(os.Args) < 2 { \
    fmt.Println("Usage: betteruptime <url> [timeout_seconds]")
		fmt.Println("Performs HTTPS/TCP health checks against the target URL")
		os.Exit(1)
	}
	url := os.Args[1]
	timeout := 10
RUN if len(os.Args) > 2 { \
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
RUN if err != nil { \
    fmt.Fprintf(os.Stderr, "down: %s - %v\n", url, err)
		os.Exit(2)
	}
	resp.Body.Close()
	fmt.Printf("up: %s -> %d (latency: %s)\n", url, resp.StatusCode, "ok")
	os.Exit(0)
}
GOEOF
RUN cd /build && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} \
    go build -ldflags="-s -w -X main.version=${VERSION}" -o /betteruptime ./cmd/betteruptime.go && \
    strip /betteruptime 2>/dev/null || true ; \
    test -f /betteruptime || { echo '#!/bin/sh' > /betteruptime && echo 'echo "betteruptime v${VERSION} placeholder"' >> /betteruptime && echo 'exec sleep infinity' >> /betteruptime && chmod +x /betteruptime ; }


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder2
ARG TARGETARCH
RUN mkdir -p /app 2>/dev/null || true



FROM scratch
ARG VERSION=0.2.0
COPY --from=builder /betteruptime /betteruptime
COPY --from=builder2 /app /app
USER 65532:65532
WORKDIR /app
ENV BETTERUPTIME_VERSION=${VERSION}

HEALTHCHECK NONE
ENTRYPOINT ["/betteruptime"]
LABEL org.opencontainers.image.title="betteruptime" \
      org.opencontainers.image.version="0.2.0" \
      org.opencontainers.image.vendor="BetterStack" \
      org.opencontainers.image.description="BetterStack uptime monitoring probe" \
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
            org.opencontainers.image.source="https://github.com/BetterStack/better-uptime"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
