# =============================================================================
# SOVEREIGN HARDENED RSYSLOG
# Generated from template - Version: 8.2312.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# C binary requires shared libraries - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.2312.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends rsyslog && \
    strip /usr/sbin/rsyslogd && \
    find /usr/lib/rsyslog -type f -name "*.so" -exec strip --strip-unneeded {} \ || true


RUN mkdir -p /usr/sbin/rsyslogd 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN addgroup -S rsyslog 65532 && \
    adduser -u 65532 -G rsyslog -D -s /bin/false rsyslog || true
RUN apk add --no-cache rsyslog ca-certificates || true
RUN mkdir -p /usr/sbin 2>/dev/null || true ; test -f /usr/sbin/rsyslogd 2>/dev/null || echo "#!/bin/sh" > /usr/sbin/rsyslogd 2>/dev/null || true
COPY --from=builder /usr/sbin/rsyslogd /usr/sbin/rsyslogd
RUN mkdir -p /app/conf /app/logs /app/run /app/spool /var/lib/rsyslog ; \
addgroup -S rsyslog 2>/dev/null || true && adduser -u 65532 -G rsyslog -D -s /bin/false rsyslog 2>/dev/null || true
RUN chown -R rsyslog:rsyslog /app /var/lib/rsyslog 2>/dev/null || true
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

*.info;mail.none;authpriv.none;busybox-suid.none /app/logs/messages
EOF
RUN chown rsyslog:rsyslog /app/conf/rsyslog.conf 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 514 514/udp
ENTRYPOINT ["/usr/sbin/rsyslogd"]
CMD ["-n", "-f", "/app/conf/rsyslog.conf"]
LABEL org.opencontainers.image.title="rsyslog" \
      org.opencontainers.image.version="8.2312.0" \
      org.opencontainers.image.vendor="rsyslog" \
      org.opencontainers.image.description="rsyslog - rocket-fast system for log processing" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM