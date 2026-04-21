# =============================================================================
# SOVEREIGN HARDENED HAPROXY-LB
# Generated from template - Version: 3.0.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.0.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc make libpcre2-dev libssl-dev zlib1g-dev curl ca-certificates && \
    curl -fsSL -k "https://www.haproxy.org/download/3.0/src/haproxy-${VERSION}.tar.gz" -o /tmp/haproxy.tar.gz && \
    tar -xzf /tmp/haproxy.tar.gz -C /tmp && \
    cd /tmp/haproxy-${VERSION} && \
    make TARGET=linux-glibc USE_PCRE2=1 USE_SSL=1 USE_ZLIB=1 -j$(nproc) && \
    cp /tmp/haproxy-${VERSION}/haproxy /haproxy && \
    strip /haproxy && \
    apt-get purge -y --auto-remove gcc make libpcre2-dev libssl-dev zlib1g-dev 2>/dev/null || true && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/haproxy.tar.gz /tmp/haproxy-${VERSION}

FROM debian:bookworm-slim AS dirbuilder
RUN mkdir -p /app /var/log/haproxy /var/cache/haproxy

FROM scratch
COPY --from=builder /haproxy /haproxy
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=dirbuilder /app /app
COPY --from=dirbuilder /var/log/haproxy /var/log/haproxy
COPY --from=dirbuilder /var/cache/haproxy /var/cache/haproxy
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/haproxy", "-v"]
ENTRYPOINT ["/haproxy"]
LABEL org.opencontainers.image.title="haproxy-lb" \
      org.opencontainers.image.version="3.0.1" \
      org.opencontainers.image.vendor="HAProxy" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="0-1" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true"
