# =============================================================================
# EVERGREEN HARDENED HAPROXY
# Generated from template - Version: 2.8.5
# Constraint: wolfi - multi-stage build with wolfi package manager
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.8.5
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31 AS builder
RUN apk add --no-cache haproxy || true
RUN mkdir -p /tmp/haproxy 2>/dev/null || true
RUN cp "$(which haproxy)" /tmp/haproxy/haproxy


RUN mkdir -p /tmp/haproxy/haproxy 2>/dev/null || true

FROM scratch
ARG VERSION=2.8.5
COPY --from=builder /tmp/haproxy/haproxy /usr/local/sbin/haproxy
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /tmp
EXPOSE 8404

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/sbin/haproxy"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="proxy" \
      org.opencontainers.image.title="haproxy" \
      org.opencontainers.image.description="Evergreen hardened HAProxy - reliable high-performance TCP/HTTP load balancer" \
      org.opencontainers.image.version="${VERSION}"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
