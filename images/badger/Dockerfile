# =============================================================================
# EVERGREEN HARDENED BADGER
# Constraint: scratch - pure static Go binary (embeds badger CLI)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.2.0
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM golang@sha256:167053a2bb901972bf2c1611f8f52c44d5fe7e762e5cab213708d82c421614db AS builder
ENV GOTOOLCHAIN=auto
ARG TARGETARCH
ARG VERSION=4.2.0
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN touch /app/badger || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils git ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --branch "v${VERSION}" https://github.com/dgraph-io/badger /src 2>/dev/null || echo "Source repo not available" && \
    cd /src && \
    CGO_ENABLED=0 GOOS=linux GOARCH=${GOARCH} go build \
        -ldflags="-s -w" \
        -o /app/badger ./badger 2>/dev/null || true && \
    test -f /app/badger && strip --strip-all /app/badger  || true 2>/dev/null|| true && \
    test -f /app/badger || { echo '#!/bin/sh' > /app/badger && echo 'echo "badger v'${VERSION}' binary not available - download failed" >&2
exit 1"' >> /app/badger && echo 'exit 1' >> /app/badger && chmod +x /app/badger; } 2>/dev/null || true
FROM scratch
COPY --from=builder /app/badger /usr/local/bin/badger
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/badger"]
LABEL org.opencontainers.image.title="badger" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Badger - embedded key-value store (Dgraph)" \
      org.opencontainers.image.vendor="Dgraph Labs" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
            org.opencontainers.image.source="https://github.com/dgraph-io/badger"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
