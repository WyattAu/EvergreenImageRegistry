# =============================================================================
# SOVEREIGN HARDENED SYSLOG-NG
# Generated from template - Version: 4.8.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# C binary requires shared libraries - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.8.1
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends syslog-ng-core && \
    strip /usr/sbin/syslog-ng && \
    find /usr/lib/syslog-ng -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true && \
    find /usr/lib/*/syslog-ng -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true

FROM debian:bookworm-20240101-slim
RUN groupadd -g 65534 syslogng && \
    useradd -m -u 65534 -g syslogng -s /usr/sbin/nologin syslogng
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        syslog-ng-core \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/sbin/syslog-ng /usr/sbin/syslog-ng
RUN mkdir -p /app/conf /app/logs /app/run /var/lib/syslog-ng && \
    chown -R syslogng:syslogng /app /var/lib/syslog-ng
COPY <<'EOF' /app/conf/syslog-ng.conf
@version: 4.8
source s_network {
    tcp(port(514) max-connections(1024));
    udp(port(514));
};
destination d_file {
    file("/app/logs/messages" perm(0644));
};
log {
    source(s_network);
    destination(d_file);
};
EOF
RUN chown syslogng:syslogng /app/conf/syslog-ng.conf
USER 65534:65534
WORKDIR /app
EXPOSE 514 514/udp 6514
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/sbin/syslog-ng", "--version"]
ENTRYPOINT ["/usr/sbin/syslog-ng"]
CMD ["-f", "/app/conf/syslog-ng.conf", "--foreground", "--no-caps"]
LABEL org.opencontainers.image.title="syslog-ng" \
      org.opencontainers.image.version="4.8.1" \
      org.opencontainers.image.vendor="OneIdentity" \
      org.opencontainers.image.description="syslog-ng - high-performance log management daemon" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-rolling" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER" \
      sovereign.hft.runtime="c"
