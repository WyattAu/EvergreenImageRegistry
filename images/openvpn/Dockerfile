# =============================================================================
# EVERGREEN HARDENED OPENVPN
# Generated from template - Version: 2.6.10
# Constraint: wolfi - Chainguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=2.6.10
ARG TARGETARCH
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS downloader
RUN apk add --no-cache openvpn || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
RUN apk add --no-cache ca-certificates && \
    adduser -D -u 65532 appuser 2>/dev/null || true && \
    mkdir -p /app /var/log/openvpn /var/cache/openvpn 2>/dev/null || true
USER appuser
WORKDIR /app
COPY --from=downloader /usr/sbin/openvpn /usr/local/bin/openvpn
EXPOSE 1194

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:1194/ || exit 1
ENTRYPOINT ["/usr/local/bin/openvpn"]
LABEL org.opencontainers.image.title="openvpn" \
      org.opencontainers.image.description="openvpn container image" \
      org.opencontainers.image.version="2.6.10" \
      org.opencontainers.image.vendor="OpenVPN" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.wolfi="true" \
            org.opencontainers.image.source="https://github.com/OpenVPN/openvpn"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
