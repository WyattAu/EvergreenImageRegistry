# =============================================================================
# SOVEREIGN HARDENED POWERDNS-API (pdns-api)
# PowerDNS authoritative DNS with REST API
# Constraint: debian-slim - requires dynamic libs
# =============================================================================

ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    pdns-server pdns-backend-sqlite-libs && \
    rm -rf /var/lib/apt/lists/*
RUN find /usr/sbin -type f -name "pdns_server" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr/sbin -type f -name "pdnsutil" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr/lib -type f -name "lib*.so*" -exec strip --strip-unneeded {} \; 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache sqlite-libs ca-certificates
RUN mkdir -p /app /var/log/pdns /var/lib/pdns /etc/pdns
COPY --from=installer /usr/sbin/pdns_server /usr/local/bin/pdns_server
COPY --from=installer /usr/sbin/pdnsutil /usr/local/bin/pdnsutil
COPY --from=installer /usr/lib/pdns /usr/lib/pdns
RUN chown -R 65532:65532 /app /var/log/pdns /var/lib/pdns
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 8081
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
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM