FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=5.7.6
RUN apk add --no-cache knot-resolver knot-resolver-utils ca-certificates || true && \
    addgroup -S -g 10000 knot 2>/dev/null || true && \
    adduser -u 65532 -G knot -D -h /app -s /bin/false knot 2>/dev/null || true && \
    mkdir -p /app /var/log/knot-resolver /var/lib/knot-resolver /etc/knot-resolver /run/knot 2>/dev/null || true && \
    chown -R 65532:65532 /app /var/log/knot-resolver /var/lib/knot-resolver /etc/knot-resolver /run/knot 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 53 53/udp 8453

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:53/ || exit 1
ENTRYPOINT ["kresd"]
CMD ["-c", "/etc/knot-resolver/knot.conf"]
LABEL org.opencontainers.image.title="knot-resolver" \
      org.opencontainers.image.version="5.7.6" \
      org.opencontainers.image.vendor="CZ.NIC" \
      org.opencontainers.image.source="https://github.com/CZ-NIC/knot-resolver" \
      org.opencontainers.image.description="Full-featured DNS recursive resolver" \
      evergreen.image.tier="1" \
      evergreen.image.category="dns" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
