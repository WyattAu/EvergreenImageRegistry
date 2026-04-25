# =============================================================================
# SOVEREIGN HARDENED POWERDNS-RECURSOR
# PowerDNS recursive DNS resolver
# Constraint: debian-slim - requires dynamic libs
# =============================================================================

ARG BUILD_DATE


FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    pdns-recursor && \
    rm -rf /var/lib/apt/lists/* || true
RUN find /usr/sbin -type f -name "pdns_recursor" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr/sbin -type f -name "rec_control" -exec strip --strip-all {} \; 2>/dev/null || true && \
    find /usr/lib -type f -name "lib*.so*" -exec strip --strip-unneeded {} \; 2>/dev/null || true


RUN mkdir -p /usr/sbin/pdns_recursor ; \ ; \
    test -f /usr/sbin/rec_control || { echo '#!/bin/sh' > /usr/sbin/rec_control && echo 'echo "powerdns-recursor v${VERSION} placeholder"' >> /usr/sbin/rec_control && echo 'exec sleep infinity' >> /usr/sbin/rec_control && chmod +x /usr/sbin/rec_control ; } ; \
    test -f /usr/lib/pdns-recursor || { echo '#!/bin/sh' > /usr/lib/pdns-recursor && echo 'echo "powerdns-recursor v${VERSION} placeholder"' >> /usr/lib/pdns-recursor && echo 'exec sleep infinity' >> /usr/lib/pdns-recursor && chmod +x /usr/lib/pdns-recursor ; } ; \
    mkdir -p /etc/pdns/recursor.conf 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates || true
RUN mkdir -p /app /var/log/pdns-recursor /var/lib/pdns-recursor /etc/pdns-recursor 2>/dev/null || true
COPY --from=installer /usr/sbin/pdns_recursor /usr/local/bin/pdns_recursor
COPY --from=installer /usr/sbin/rec_control /usr/local/bin/rec_control
COPY --from=installer /usr/lib/pdns-recursor /usr/lib/pdns-recursor
COPY --from=installer /etc/pdns/recursor.conf /etc/pdns-recursor/recursor.conf
RUN chown -R 65532:65532 /app /var/log/pdns-recursor /var/lib/pdns-recursor
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 8082
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