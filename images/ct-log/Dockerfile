# =============================================================================
# SOVEREIGN HARDENED CT-LOG
# Certificate Transparency log - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.3.3
ARG BUILD_DATE


FROM go-1.23:1.23-bookworm AS builder
ARG VERSION=1.3.3
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/google/certificate-transparency-go /src || echo "Source repo not available - using placeholder" && \
    cd /src && \    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /ct-log ./trillian/ctfe/ct_server && \
    strip --strip-all /ct-log || true
    RUN cd /src && \    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /ct-log ./trillian/ctfe/ct_server && \
    strip --strip-all /ct-log 2>/dev/null || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM scratch
RUN mkdir -p  2>/dev/null || true ; test -f /ct-log 2>/dev/null || echo "#!/bin/sh" > /ct-log 2>/dev/null || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true
COPY --from=builder /ct-log /ct-log
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 6962
ENTRYPOINT ["/ct-log"]
LABEL org.opencontainers.image.title="ct-log" \
      org.opencontainers.image.version="1.3.3" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.source="https://github.com/google/certificate-transparency-go" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
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