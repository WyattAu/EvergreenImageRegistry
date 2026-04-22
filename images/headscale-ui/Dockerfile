# =============================================================================
# SOVEREIGN HARDENED HEADSCALE UI
# Headscale web management dashboard (static assets)
# Constraint: distroless - serve static files with minimal Go HTTP server
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG GO_VERSION=1.22.4
ARG BUILD_DATE

FROM golang:${GO_VERSION}-bookworm AS server-builder
RUN mkdir -p /src
COPY <<'GOSRC' /src/main.go
package main

import (
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	dir := "/www"
	port := "8080"
	if p := os.Getenv("PORT"); p != "" {
		port = p
	}

	fs := http.FileServer(http.Dir(dir))
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		path := filepath.Join(dir, filepath.Clean(r.URL.Path))
		if _, err := os.Stat(path); os.IsNotExist(err) {
			http.ServeFile(w, r, filepath.Join(dir, "index.html"))
			return
		}
		if strings.HasSuffix(r.URL.Path, ".js") || strings.HasSuffix(r.URL.Path, ".css") {
			w.Header().Set("Cache-Control", "public, max-age=86400")
		}
		fs.ServeHTTP(w, r)
	})

	log.Printf("Headscale UI serving on :%s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}
GOSRC
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -trimpath -o /fileserver /src/main.go && \
    strip --strip-all /fileserver

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/gurucomputing/headscale-ui/releases/download/2024.1.1/headscale-ui-2024.1.1.tar.gz" -o /dist.tar.gz && \
    mkdir -p /www && tar -xzf /dist.tar.gz -C /www/ --strip-components=1 && \
    rm -rf /dist.tar.gz

FROM gcr.io/distroless/static-debian12
COPY --from=server-builder /fileserver /fileserver
COPY --from=downloader /www /www
USER 65532:65532
WORKDIR /www
EXPOSE 8080
ENTRYPOINT ["/fileserver"]
LABEL org.opencontainers.image.title="headscale-ui" \
      org.opencontainers.image.version="2024.1.1" \
      org.opencontainers.image.vendor="gurucomputing" \
      org.opencontainers.image.source="https://github.com/gurucomputing/headscale-ui" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distrole="distroless" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="distroless"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM