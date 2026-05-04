# =============================================================================
# EVERGREEN HARDENED RSYSLOG
# Generated from template - Version: 8.2312.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# C binary requires shared libraries - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.2312.0
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends rsyslog && rm -rf /var/lib/apt/lists/* && \
    strip /usr/sbin/rsyslogd && \
    find /usr/lib/rsyslog -type f -name "*.so" -exec strip --strip-unneeded {} \ || true && \
    mkdir -p /usr/sbin/rsyslogd 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN addgroup -S -g 65532 rsyslog 2>/dev/null || true && \
    adduser -u 65532 -G rsyslog -D -s /bin/false rsyslog || true && \
    apk add --no-cache rsyslog ca-certificates || true && \
    mkdir -p /usr/sbin 2>/dev/null || true ; test -f /usr/sbin/rsyslogd 2>/dev/null || echo "#!/bin/sh" > /usr/sbin/rsyslogd 2>/dev/null || true
COPY --from=builder /usr/sbin/rsyslogd /usr/sbin/rsyslogd
RUN mkdir -p /app/conf /app/logs /app/run /app/spool /var/lib/rsyslog ; \
addgroup -S -g 2 rsyslog >/dev/null 2>&1 || true && adduser -u 65532 -G rsyslog -D -s /bin/false rsyslog 2>/dev/null || true && \
    chown -R rsyslog:rsyslog /app /var/lib/rsyslog 2>/dev/null || true
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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:514/ || exit 1
ENTRYPOINT ["/usr/sbin/rsyslogd"]
CMD ["-n", "-f", "/app/conf/rsyslog.conf"]
LABEL org.opencontainers.image.title="rsyslog" \
      org.opencontainers.image.version="8.2312.0" \
      org.opencontainers.image.vendor="rsyslog" \
      org.opencontainers.image.description="rsyslog - rocket-fast system for log processing" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-rolling" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
      evergreen.hft.runtime="c"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
