# =============================================================================
# EVERGREEN HARDENED HAPROXY LB
# Generated from template - Version: 2.8.5
# Constraint: wolfi - multi-stage build with wolfi package manager
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.8.5
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v0.3.0

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
RUN apk add --no-cache haproxy ca-certificates && \
    mkdir -p /tmp/haproxy 2>/dev/null || true && \
    cp "$(which haproxy)" /tmp/haproxy/haproxy && \
    mkdir -p /tmp/haproxy/haproxy 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=2.8.5
COPY --from=builder /tmp/haproxy/haproxy /usr/local/sbin/haproxy
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /tmp
EXPOSE 80 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/shim", "run"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="load-balancer" \
      org.opencontainers.image.title="haproxy-lb" \
      org.opencontainers.image.description="Evergreen hardened HAProxy LB - dedicated load balancer configuration variant" \
      org.opencontainers.image.version="${VERSION}" \
            org.opencontainers.image.source="https://github.com/haproxy/haproxy"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
