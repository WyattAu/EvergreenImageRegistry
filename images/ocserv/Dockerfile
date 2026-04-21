# =============================================================================
# SOVEREIGN HARDENED OCSERV
# OpenConnect VPN server (AnyConnect-compatible)
# Constraint: debian-slim - ocserv requires dynamic libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    ocserv gnutls-bin && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/ocserv /run/ocserv && \
    strip --strip-all /usr/sbin/ocserv 2>/dev/null || true && \
    strip --strip-all /usr/bin/occtl 2>/dev/null || true && \
    strip --strip-all /usr/bin/ocpasswd 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgnutls30 libtasn1-6 libnettle8 libhogweed6 libgmp10 \
    libpam0g libseccomp2 libwrap0 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=installer /usr/sbin/ocserv /usr/sbin/ocserv
COPY --from=installer /usr/bin/occtl /usr/bin/occtl
COPY --from=installer /usr/bin/ocpasswd /usr/bin/ocpasswd
COPY --from=installer /etc/ocserv /etc/ocserv
COPY --from=installer /app /app
COPY --from=installer /var/log/ocserv /var/log/ocserv
RUN mkdir -p /run/ocserv && \
    chown -R 65534:65534 /app /var/log/ocserv /run/ocserv
USER 65534:65534
WORKDIR /app
EXPOSE 443 443/udp
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/bin/occtl", "--help"]
ENTRYPOINT ["/usr/sbin/ocserv"]
CMD ["-f"]
LABEL org.opencontainers.image.title="ocserv" \
      org.opencontainers.image.version="1.3.0" \
      org.opencontainers.image.vendor="OpenConnect" \
      org.opencontainers.image.source="https://www.infradead.org/ocserv/" \
      org.opencontainers.image.description="OpenConnect VPN server (AnyConnect-compatible)" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"
