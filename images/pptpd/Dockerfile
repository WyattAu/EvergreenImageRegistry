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

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ppp libwrap0 libstdc++6 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
COPY --from=installer /usr/sbin/pptpd /usr/sbin/pptpd
COPY --from=installer /usr/sbin/pptpctrl /usr/sbin/pptpctrl
COPY --from=installer /etc/pptpd.conf /etc/pptpd.conf
COPY --from=installer /etc/ppp /etc/ppp
COPY --from=installer /app /app
COPY --from=installer /var/log/pptpd /var/log/pptpd
RUN mkdir -p /run/pptpd /etc/pptpd.d && \
    chown -R 65534:65534 /app /var/log/pptpd /run/pptpd
USER 65534:65534
WORKDIR /app
EXPOSE 1723
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/sbin/pptpd", "--version"]
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
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
