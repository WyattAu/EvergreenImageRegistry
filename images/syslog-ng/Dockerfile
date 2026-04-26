# =============================================================================
# SOVEREIGN HARDENED SYSLOG-NG
# Generated from template - Version: 4.8.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# C binary requires shared libraries - cannot use scratch
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.8.1
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends syslog-ng-core && \
    strip /usr/sbin/syslog-ng && \
    find /usr/lib/syslog-ng -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true && \
    find /usr/lib/*/syslog-ng -type f -name "*.so" -exec strip --strip-unneeded {} \; 2>/dev/null || true


RUN mkdir -p /usr/sbin/syslog-ng 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN addgroup -S 65532 syslogng && \
    adduser -u 65532 -G syslogng -D -s /bin/false syslogng || true
RUN apk add --no-cache ca-certificates 
COPY --from=builder /usr/sbin/syslog-ng /usr/sbin/syslog-ng
RUN mkdir -p /app/conf /app/logs /app/run /var/lib/syslog-ng ; \
    RUN addgroup -S syslogng 2>/dev/null || true && adduser -u 65532 -G syslogng -D -s /bin/false syslogng 2>/dev/null || true
    RUN chown -R syslogng:syslogng /app /var/lib/syslog-ng
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
RUN EOF
RUN chown syslogng:syslogng /app/conf/syslog-ng.conf
USER 65532:65532
WORKDIR /app
EXPOSE 514 514/udp 6514
ENTRYPOINT ["/usr/sbin/syslog-ng"]
CMD ["-f", "/app/conf/syslog-ng.conf", "--foreground", "--no-caps"]
LABEL org.opencontainers.image.title="syslog-ng" \
      org.opencontainers.image.version="4.8.1" \
      org.opencontainers.image.vendor="OneIdentity" \
      org.opencontainers.image.description="syslog-ng - high-performance log management daemon" \
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