# =============================================================================
# SOVEREIGN HARDENED POWERDNS-RECURSOR
# PowerDNS recursive DNS resolver
# Constraint: debian-slim - requires dynamic libs
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    pdns-recursor && \
    rm -rf /var/lib/apt/lists/*
RUN find /usr/sbin -type f -name "pdns_recursor" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr/sbin -type f -name "rec_control" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr/lib -type f -name "lib*.so*" -exec strip --strip-unneeded {} \; 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 libboost-system1.74.0 libboost-filesystem1.74.0 \
    libboost-program-options1.74.0 libboost-thread1.74.0 \
    libluajit-5.1-2 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/pdns-recursor /var/lib/pdns-recursor /etc/pdns-recursor
COPY --from=installer /usr/sbin/pdns_recursor /usr/local/bin/pdns_recursor
COPY --from=installer /usr/sbin/rec_control /usr/local/bin/rec_control
COPY --from=installer /usr/lib/pdns-recursor /usr/lib/pdns-recursor
COPY --from=installer /etc/pdns/recursor.conf /etc/pdns-recursor/recursor.conf 2>/dev/null || true
RUN chown -R 65534:65534 /app /var/log/pdns-recursor /var/lib/pdns-recursor
USER 65534:65534
WORKDIR /app
EXPOSE 53 53/udp 8082
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/rec_control", "ping"]
ENTRYPOINT ["/usr/local/bin/pdns_recursor"]
LABEL org.opencontainers.image.title="powerdns-recursor" \
      org.opencontainers.image.version="bookworm" \
      org.opencontainers.image.vendor="PowerDNS" \
      org.opencontainers.image.source="https://github.com/PowerDNS/pdns" \
      org.opencontainers.image.description="PowerDNS recursive DNS resolver" \
      sovereign.image.tier="1" \
      sovereign.image.category="dns" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"
