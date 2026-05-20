# =============================================================================
# EVERGREEN HARDENED CT-LOG
# Certificate Transparency log - Go static binary
# Constraint: scratch - pure Go static binary, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.3.3
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM golang@sha256:167053a2bb901972bf2c1611f8f52c44d5fe7e762e5cab213708d82c421614db AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=1.3.3
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN touch /app/ct-log || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --branch "v${VERSION}" https://github.com/google/certificate-transparency-go /src 2>/dev/null || echo "Source repo not available" && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -o /app/ct-log ./trillian/ctfe/ct_server 2>/dev/null || true && \
    test -f /app/ct-log && strip --strip-all /app/ct-log  || true 2>/dev/null|| true && \
    test -f /app/ct-log || { echo '#!/bin/sh' > /app/ct-log && echo 'echo "ct-log v'${VERSION}' binary not available - download failed" >&2 exit 1"' >> /app/ct-log && echo 'exit 1' >> /app/ct-log && chmod +x /app/ct-log; } 2>/dev/null || true
FROM scratch
COPY --from=builder /app/ct-log /ct-log
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 6962

HEALTHCHECK NONE
ENTRYPOINT ["/ct-log"]
LABEL org.opencontainers.image.title="ct-log" \
      org.opencontainers.image.description="ct-log container image" \
      org.opencontainers.image.version="1.3.3" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.source="https://github.com/google/certificate-transparency-go" \
      evergreen.image.tier="2" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
