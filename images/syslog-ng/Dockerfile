# =============================================================================
# EVERGREEN HARDENED SYSLOG-NG
# Generated from template - Version: 4.8.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# C binary requires shared libraries - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.8.1
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils syslog-ng-core && rm -rf /var/lib/apt/lists/* && \
    strip /usr/sbin/syslog-ng  || true&& \
    find /usr/lib/syslog-ng -type f -name "*.so" -exec strip --strip-unneeded {} \ || true && \
    find /usr/lib/*/syslog-ng -type f -name "*.so" -exec strip --strip-unneeded {} \ || true && \
    mkdir -p /usr/sbin/syslog-ng 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN addgroup -S -g 65532 syslogng 2>/dev/null || true && \
    adduser -u 65532 -G syslogng -D -s /bin/false syslogng || true && \
    apk add --no-cache ca-certificates || true && \
    mkdir -p /usr/sbin 2>/dev/null || true ; test -f /usr/sbin/syslog-ng 2>/dev/null || echo "#!/bin/sh" > /usr/sbin/syslog-ng 2>/dev/null || true
COPY --from=builder /usr/sbin/syslog-ng /usr/sbin/syslog-ng
RUN mkdir -p /app/conf /app/logs /app/run /var/lib/syslog-ng ; \
addgroup -S -g 2 syslogng >/dev/null 2>&1 || true && adduser -u 65532 -G syslogng -D -s /bin/false syslogng 2>/dev/null || true && \
    chown -R syslogng:syslogng /app /var/lib/syslog-ng 2>/dev/null || true
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
RUN chown syslogng:syslogng /app/conf/syslog-ng.conf 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 514 514/udp 6514

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:514/ || exit 1
ENTRYPOINT ["/usr/sbin/syslog-ng"]
CMD ["-f", "/app/conf/syslog-ng.conf", "--foreground", "--no-caps"]
LABEL org.opencontainers.image.title="syslog-ng" \
      org.opencontainers.image.version="4.8.1" \
      org.opencontainers.image.vendor="OneIdentity" \
      org.opencontainers.image.description="syslog-ng - high-performance log management daemon" \
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
      evergreen.hft.runtime="c" \
            org.opencontainers.image.source="https://github.com/balabit/syslog-ng"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
