# =============================================================================
# SOVEREIGN HARDENED HAPROXY DEV
# Generated from template - Version: 2.8.5
# Constraint: wolfi - multi-stage build with wolfi package manager
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.8.5
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base:latest AS builder
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
ENTRYPOINT ["/usr/local/sbin/haproxy", "-f", "/dev/stdin"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="proxy" \
      org.opencontainers.image.title="haproxy-dev" \
      org.opencontainers.image.description="Sovereign hardened HAProxy dev - experimental development configuration variant" \
      org.opencontainers.image.version="${VERSION}"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
