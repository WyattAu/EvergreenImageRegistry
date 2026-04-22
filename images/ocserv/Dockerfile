# =============================================================================
# SOVEREIGN HARDENED OCSERV
# OpenConnect VPN server (AnyConnect-compatible)
# Constraint: debian-slim - ocserv requires dynamic libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.3.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    ocserv gnutls-bin && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/ocserv /run/ocserv && \
    strip --strip-all /usr/sbin/ocserv 2>/dev/null || true && \
    strip --strip-all /usr/bin/occtl 2>/dev/null || true && \
    strip --strip-all /usr/bin/ocpasswd 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates
COPY --from=installer /usr/sbin/ocserv /usr/sbin/ocserv
COPY --from=installer /usr/bin/occtl /usr/bin/occtl
COPY --from=installer /usr/bin/ocpasswd /usr/bin/ocpasswd
COPY --from=installer /etc/ocserv /etc/ocserv
COPY --from=installer /app /app
COPY --from=installer /var/log/ocserv /var/log/ocserv
RUN mkdir -p /run/ocserv && \
    chown -R 65532:65532 /app /var/log/ocserv /run/ocserv
USER 65532:65532
WORKDIR /app
EXPOSE 443 443/udp
ENTRYPOINT ["/usr/sbin/ocserv"]
CMD ["-f"]
LABEL org.opencontainers.image.title="ocserv" \
      org.opencontainers.image.version="1.3.0" \
      org.opencontainers.image.vendor="OpenConnect" \
      org.opencontainers.image.source="https://www.infradead.org/ocserv/" \
      org.opencontainers.image.description="OpenConnect VPN server (AnyConnect-compatible)" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
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