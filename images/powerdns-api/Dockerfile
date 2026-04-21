# =============================================================================
# SOVEREIGN HARDENED POWERDNS-API (pdns-api)
# PowerDNS authoritative DNS with REST API
# Constraint: debian-slim - requires dynamic libs
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    pdns-server pdns-backend-sqlite3 && \
    rm -rf /var/lib/apt/lists/*
RUN find /usr/sbin -type f -name "pdns_server" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr/sbin -type f -name "pdnsutil" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr/lib -type f -name "lib*.so*" -exec strip --strip-unneeded {} \; 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 libboost-system1.74.0 libboost-filesystem1.74.0 \
    libboost-program-options1.74.0 libboost-thread1.74.0 \
    libsqlite3-0 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/pdns /var/lib/pdns /etc/pdns
COPY --from=installer /usr/sbin/pdns_server /usr/local/bin/pdns_server
COPY --from=installer /usr/sbin/pdnsutil /usr/local/bin/pdnsutil
COPY --from=installer /usr/lib/pdns /usr/lib/pdns
RUN chown -R 65534:65534 /app /var/log/pdns /var/lib/pdns
USER 65534:65534
WORKDIR /app
EXPOSE 53 53/udp 8081
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/pdns_server", "--version"]
ENTRYPOINT ["/usr/local/bin/pdns_server"]
LABEL org.opencontainers.image.title="powerdns-api" \
      org.opencontainers.image.version="bookworm" \
      org.opencontainers.image.vendor="PowerDNS" \
      org.opencontainers.image.source="https://github.com/PowerDNS/pdns" \
      org.opencontainers.image.description="PowerDNS authoritative DNS with REST API" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"
