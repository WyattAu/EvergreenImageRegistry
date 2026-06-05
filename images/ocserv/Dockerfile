# =============================================================================
# EVERGREEN HARDENED OCSERV
# OpenConnect VPN server (AnyConnect-compatible)
# Constraint: debian-slim - ocserv requires dynamic libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.3.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    ocserv gnutls-bin && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app /var/log/ocserv /run/ocserv ; \
    strip --strip-all /usr/sbin/ocserv 2>/dev/null 2>/dev/null && \
    strip --strip-all /usr/bin/occtl 2>/dev/null 2>/dev/null && \
    strip --strip-all /usr/bin/ocpasswd 2>/dev/null 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache ca-certificates
COPY --from=installer /usr/sbin/ocserv /usr/sbin/ocserv
COPY --from=installer /usr/bin/occtl /usr/bin/occtl
COPY --from=installer /usr/bin/ocpasswd /usr/bin/ocpasswd
COPY --from=installer /etc/ocserv /etc/ocserv
COPY --from=installer /app /app
COPY --from=installer /var/log/ocserv /var/log/ocserv
RUN mkdir -p /run/ocserv ; \
    chown -R 65532:65532 /app /var/log/ocserv /run/ocserv
USER 65532:65532
WORKDIR /app
EXPOSE 443 443/udp

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:443"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/sbin/ocserv", "--", "-f"]
LABEL org.opencontainers.image.title="ocserv" \
      org.opencontainers.image.version="1.3.0" \
      org.opencontainers.image.vendor="OpenConnect" \
      org.opencontainers.image.source="https://www.infradead.org/ocserv/" \
      org.opencontainers.image.description="OpenConnect VPN server (AnyConnect-compatible)" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
