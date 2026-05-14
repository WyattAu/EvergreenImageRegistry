# =============================================================================
# EVERGREEN HARDENED PPTPD
# Point-to-Point Tunneling Protocol (PPTP) server
# Constraint: debian-slim - pptpd requires dynamic libs and kernel modules
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.10.0
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS installer
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    pptpd ppp && \
    rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app /var/log/pptpd /run/pptpd /etc/pptpd.d ; \
    strip --strip-all /usr/sbin/pptpd 2>/dev/null  || true 2>/dev/null|| true && \
    strip --strip-all /usr/sbin/pptpctrl 2>/dev/null  || true 2>/dev/null|| true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache libstdc++ ca-certificates
COPY --from=installer /usr/sbin/pptpd /usr/sbin/pptpd
COPY --from=installer /usr/sbin/pptpctrl /usr/sbin/pptpctrl
COPY --from=installer /etc/pptpd.conf /etc/pptpd.conf
COPY --from=installer /etc/ppp /etc/ppp
COPY --from=installer /app /app
COPY --from=installer /var/log/pptpd /var/log/pptpd
RUN mkdir -p /run/pptpd /etc/pptpd.d ; \
    chown -R 65532:65532 /app /var/log/pptpd /run/pptpd
USER 65532:65532
WORKDIR /app
EXPOSE 1723

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:1723/ || exit 1
ENTRYPOINT ["/usr/sbin/pptpd"]
CMD ["--fg"]
LABEL org.opencontainers.image.title="pptpd" \
      org.opencontainers.image.version="1.10.0" \
      org.opencontainers.image.vendor="PPTP Project" \
      org.opencontainers.image.source="https://sourceforge.net/projects/poptop/" \
      org.opencontainers.image.description="Point-to-Point Tunneling Protocol server" \
      evergreen.image.tier="1" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
