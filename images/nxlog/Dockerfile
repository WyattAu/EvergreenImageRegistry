ARG VERSION=latest

FROM nxlog/nxlog:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN addgroup -S -g 65532 nxlog 2>/dev/null || true && \
    adduser -u 65532 -G nxlog -D -s /bin/false nxlog 2>/dev/null || true && \
    apk add --no-cache curl libzstd1 zlib expat ca-certificates || true && \
    mkdir -p /opt /opt/nxlog/bin 2>/dev/null || true
COPY --from=upstream /opt/nxlog /opt/nxlog
RUN mkdir -p /app/conf /app/logs /app/data /var/lib/nxlog ; \
    chown -R nxlog:nxlog /app /opt/nxlog /var/lib/nxlog


WORKDIR /app

EXPOSE 514 514/udp
EXPOSE 9101

LABEL org.opencontainers.image.title="nxlog" org.opencontainers.image.version="3.1.2331" org.opencontainers.image.vendor="nxlog" org.opencontainers.image.description="NXLog Community Edition - log collection and forwarding" evergreen.image.tier="1" evergreen.constraint.nonroot="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="5s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="5000ms" evergreen.hft.cpu-pins="4-5" evergreen.hft.cpu-pins-mode="shared" evergreen.hft.deploy-strategy="standard-rolling" evergreen.hft.pre-stop-hook="true" evergreen.hft.pre-stop-delay="5s" evergreen.hft.connection-drain="true" evergreen.hft.sched-policy="SCHED_OTHER" evergreen.hft.runtime="c" \
      org.opencontainers.image.source="https://github.com/nxlog/nxlog-ce"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:514/ || exit 1
ENTRYPOINT ["/opt/nxlog/bin/nxlog"]

CMD ["-c", "/app/conf/nxlog.conf"]
