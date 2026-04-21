# =============================================================================
# SOVEREIGN HARDENED STRONGSWAN
# Generated from template - Version: 6.0.1
# Constraint: debian-slim - StrongSwan requires build from source
# =============================================================================

ARG VERSION=6.0.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc make libssl-dev libgmp-dev curl ca-certificates && \
    curl -fsSL -k "https://download.strongswan.org/strongswan-${VERSION}.tar.gz" -o /tmp/strongswan.tar.gz && \
    tar -xzf /tmp/strongswan.tar.gz -C /tmp && \
    cd /tmp/strongswan-${VERSION} && \
    ./configure --prefix=/opt/strongswan --enable-charon --enable-swanctl && \
    make -j$(nproc) && \
    make install && \
    strip /opt/strongswan/sbin/charon 2>/dev/null || true && \
    apt-get purge -y --auto-remove gcc make libssl-dev libgmp-dev 2>/dev/null || true && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/strongswan.tar.gz /tmp/strongswan-${VERSION}

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 libgmp10 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' strongswan 2>/dev/null || true
RUN mkdir -p /app /var/log/charon /var/cache/charon
USER strongswan
WORKDIR /app
COPY --from=builder /opt/strongswan /opt/strongswan
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
EXPOSE 500 4500
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /opt/strongswan/sbin/ipsec status
ENTRYPOINT ["/opt/strongswan/sbin/charon"]
LABEL org.opencontainers.image.title="strongswan" \
      org.opencontainers.image.version="6.0.1" \
      org.opencontainers.image.vendor="StrongSwan" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true"
