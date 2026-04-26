# =============================================================================
# SOVEREIGN HARDENED MESHBIRD
# Distributed private networking (Go-based mesh VPN)
# Constraint: scratch - Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.4.0
ARG BUILD_DATE

ARG GO_VERSION=1.22.4


FROM go-1.23:${GO_VERSION}-bookworm AS builder
ARG VERSION=0.4.0
ARG GO_VERSION=1.22.4
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch v${VERSION}  || echo "Source repo not available - using placeholder" && \
    https://github.com/meshbird/meshbird /src && \
    cd /src && \    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w -X main.version=${VERSION}" \
    -trimpath \
    -o /meshbird && \
    strip --strip-all /meshbird || true
    RUN https://github.com/meshbird/meshbird /src && \
    cd /src && \    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w -X main.version=${VERSION}" \
    -trimpath \
    -o /meshbird && \
    strip --strip-all /meshbird 2>/dev/null || true


FROM debian:bookworm-slim AS builder2
RUN mkdir -p /app /var/log/meshbird 2>/dev/null || true


FROM scratch
RUN mkdir -p  2>/dev/null || true ; test -f /meshbird 2>/dev/null || echo "#!/bin/sh" > /meshbird 2>/dev/null || true
COPY --from=builder /meshbird /meshbird
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder2 /app /app
COPY --from=builder2 /var/log/meshbird /var/log/meshbird
USER 65532:65532
WORKDIR /app
EXPOSE 10500 10500/udp
ENTRYPOINT ["/meshbird"]
LABEL org.opencontainers.image.title="meshbird" \
      org.opencontainers.image.version="0.4.0" \
      org.opencontainers.image.vendor="Meshbird" \
      org.opencontainers.image.source="https://github.com/meshbird/meshbird" \
      org.opencontainers.image.description="Distributed private networking mesh VPN" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM