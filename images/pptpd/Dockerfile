# =============================================================================
# SOVEREIGN HARDENED PPTPD
# Point-to-Point Tunneling Protocol (PPTP) server
# Constraint: debian-slim - pptpd requires dynamic libs and kernel modules
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.10.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    pptpd ppp && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/pptpd /run/pptpd /etc/pptpd.d && \
    strip --strip-all /usr/sbin/pptpd 2>/dev/null || true && \
    strip --strip-all /usr/sbin/pptpctrl 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libstdc++ ca-certificates
COPY --from=installer /usr/sbin/pptpd /usr/sbin/pptpd
COPY --from=installer /usr/sbin/pptpctrl /usr/sbin/pptpctrl
COPY --from=installer /etc/pptpd.conf /etc/pptpd.conf
COPY --from=installer /etc/ppp /etc/ppp
COPY --from=installer /app /app
COPY --from=installer /var/log/pptpd /var/log/pptpd
RUN mkdir -p /run/pptpd /etc/pptpd.d && \
    chown -R 65532:65532 /app /var/log/pptpd /run/pptpd
USER 65532:65532
WORKDIR /app
EXPOSE 1723
ENTRYPOINT ["/usr/sbin/pptpd"]
CMD ["--fg"]
LABEL org.opencontainers.image.title="pptpd" \
      org.opencontainers.image.version="1.10.0" \
      org.opencontainers.image.vendor="PPTP Project" \
      org.opencontainers.image.source="https://sourceforge.net/projects/poptop/" \
      org.opencontainers.image.description="Point-to-Point Tunneling Protocol server" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM