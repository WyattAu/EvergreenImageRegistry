# =============================================================================
# SOVEREIGN HARDENED HAPROXY
# Generated from template - Version: 2.8.5
# Constraint: wolfi - multi-stage build with wolfi package manager
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.8.5
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM ghcr.io/wolfi-dev/os:latest AS builder
RUN apk add --no-cache haproxy
RUN mkdir -p /tmp/haproxy
RUN cp "$(which haproxy)" /tmp/haproxy/haproxy

FROM scratch
COPY --from=builder /tmp/haproxy/haproxy /usr/local/sbin/haproxy
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65534:65534
WORKDIR /tmp
EXPOSE 8404
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/sbin/haproxy", "-v"]
ENTRYPOINT ["/usr/local/sbin/haproxy"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="proxy" \
      org.opencontainers.image.title="haproxy" \
      org.opencontainers.image.description="Sovereign hardened HAProxy - reliable high-performance TCP/HTTP load balancer" \
      org.opencontainers.image.version="${VERSION}"
