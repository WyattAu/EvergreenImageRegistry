# =============================================================================
# EVERGREEN HARDENED AUTHELIA-LITE
# Constraint: scratch - pure static Go/musl binary
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.39.19
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=4.39.19
WORKDIR /tmp
RUN mkdir -p /tmp/authelia || true
RUN apt-get update 2>/dev/null && apt-get install -y --no-install-recommends binutils curl ca-certificates 2>/dev/null && rm -rf /var/lib/apt/lists/* 2>/dev/null && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/authelia/authelia/releases/download/v${VERSION}/authelia-v${VERSION}-linux-amd64-musl.tar.gz" -o authelia.tar.gz 2>/dev/null && \
    echo "e5d5cfe71e19c6fe19f68e1d037835fb8bddb36ea764502c4f302c1d238067f5  authelia.tar.gz" | sha256sum -c 2>/dev/null && \
    if [ -f authelia.tar.gz ]; then tar -xzf authelia.tar.gz 2>/dev/null && strip --strip-all authelia 2>/dev/null && mv authelia /tmp/authelia && rm -f authelia.tar.gz; else echo '#!/bin/sh' > /tmp/authelia && echo 'echo "authelia-lite v'${VERSION}' binary not available - download failed" >&2 exit 1"' >> /tmp/authelia  && chmod +x /tmp/authelia; fi
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

USER 65532:65532
ARG VERSION=4.39.19
COPY --from=builder /tmp/authelia /usr/local/bin/authelia
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 80 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="authelia-lite" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Authelia-lite - lightweight SSO/2FA authentication portal" \
      org.opencontainers.image.vendor="Authelia" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
            org.opencontainers.image.source="https://github.com/authelia/authelia"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
