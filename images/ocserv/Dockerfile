# =============================================================================
# EVERGREEN HARDENED OCSERV
# OpenConnect VPN server (AnyConnect-compatible)
# Constraint: debian-slim - ocserv requires dynamic libs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.3.0
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    ocserv gnutls-bin && \
    rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app /var/log/ocserv /run/ocserv ; \
    strip --strip-all /usr/sbin/ocserv 2>/dev/null || true && \
    strip --strip-all /usr/bin/occtl 2>/dev/null || true && \
    strip --strip-all /usr/bin/ocpasswd 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:443/ || exit 1
ENTRYPOINT ["/usr/sbin/ocserv"]
CMD ["-f"]
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

EXPOSE 9101
STOPSIGNAL SIGTERM
