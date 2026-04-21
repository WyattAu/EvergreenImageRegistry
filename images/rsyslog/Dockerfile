# =============================================================================
# SOVEREIGN HARDENED RSYSLOG
# Generated from template - Version: 8.2312.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# C binary requires shared libraries - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.2312.0
ARG BUILD_DATE

FROM debian:bookworm-20240101-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends rsyslog && \
    strip /usr/sbin/rsyslogd && \
    find /usr/lib/rsyslog -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true

FROM debian:bookworm-20240101-slim
RUN groupadd -g 65534 rsyslog && \
    useradd -m -u 65534 -g rsyslog -s /usr/sbin/nologin rsyslog
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        rsyslog \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/sbin/rsyslogd /usr/sbin/rsyslogd
RUN mkdir -p /app/conf /app/logs /app/run /app/spool /var/lib/rsyslog && \
    chown -R rsyslog:rsyslog /app /var/lib/rsyslog
COPY <<'EOF' /app/conf/rsyslog.conf
module(load="imudp")
input(type="imudp" port="514")
module(load="imtcp")
input(type="imtcp" port="514")

$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
$FileOwner rsyslog
$FileGroup rsyslog
$FileCreateMode 0644
$DirCreateMode 0755

*.info;mail.none;authpriv.none;cron.none /app/logs/messages
EOF
RUN chown rsyslog:rsyslog /app/conf/rsyslog.conf
USER 65534:65534
WORKDIR /app
EXPOSE 514 514/udp
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/sbin/rsyslogd", "-v"]
ENTRYPOINT ["/usr/sbin/rsyslogd"]
CMD ["-n", "-f", "/app/conf/rsyslog.conf"]
LABEL org.opencontainers.image.title="rsyslog" \
      org.opencontainers.image.version="8.2312.0" \
      org.opencontainers.image.vendor="rsyslog" \
      org.opencontainers.image.description="rsyslog - rocket-fast system for log processing" \
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
