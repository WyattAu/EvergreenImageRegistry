# =============================================================================
# SOVEREIGN HARDENED DNSDIST
# Generated from template - Version: 1.9.6
# Constraint: debian-slim with PowerDNS apt repo (no pre-built binaries)
# =============================================================================

ARG VERSION=1.9.6
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends gnupg2 curl && \
    curl -sSL https://repo.powerdns.com/CBC8B38D-pub.asc | gpg --dearmor -o /usr/share/keyrings/dnsdist.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/dnsdist.gpg] http://repo.powerdns.com/debian bookworm-dnsdist-main" > /etc/apt/sources.list.d/dnsdist.list && \
    apt-get update && apt-get install -y --no-install-recommends dnsdist && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /usr/share/keyrings/dnsdist.gpg
RUN mkdir -p /app /var/log/dnsdist /var/cache/dnsdist
USER 65534:65534
WORKDIR /app
EXPOSE 53 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["dnsdist", "--version"]
ENTRYPOINT ["dnsdist"]
LABEL org.opencontainers.image.title="dnsdist" \
      org.opencontainers.image.version="1.9.6" \
      org.opencontainers.image.vendor="PowerDNS" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
