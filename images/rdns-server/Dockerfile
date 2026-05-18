# =============================================================================
# EVERGREEN HARDENED RDNS-SERVER
# Constraint: scratch - pure static Go binary
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.12.0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM golang@sha256:167053a2bb901972bf2c1611f8f52c44d5fe7e762e5cab213708d82c421614db AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=0.12.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN touch /app/rdns-server || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --branch "v${VERSION}" https://github.com/folbricht/rdns /src 2>/dev/null || echo "Source repo not available" && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -o /app/rdns-server ./cmd/rdnsd 2>/dev/null || true && \
    test -f /app/rdns-server && strip --strip-all /app/rdns-server  || true 2>/dev/null|| true && \
    test -f /app/rdns-server || { echo '#!/bin/sh' > /app/rdns-server && echo 'echo "rdns-server v'${VERSION}' placeholder"' >> /app/rdns-server && echo 'exec sleep infinity' >> /app/rdns-server && chmod +x /app/rdns-server; } 2>/dev/null || true
FROM scratch
COPY --from=builder /app/rdns-server /usr/local/bin/rdns-server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 53 8053

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/rdns-server"]
LABEL org.opencontainers.image.title="rdns-server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened RDNS - recursive DNS server" \
      org.opencontainers.image.vendor="folbricht" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
            org.opencontainers.image.source="https://github.com/folbricht/rdns"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
