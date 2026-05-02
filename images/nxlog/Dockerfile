ARG VERSION=latest

FROM nxlog/nxlog:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

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

LABEL org.opencontainers.image.title="nxlog" org.opencontainers.image.version="3.1.2331" org.opencontainers.image.vendor="nxlog" org.opencontainers.image.description="NXLog Community Edition - log collection and forwarding" sovereign.image.tier="1" sovereign.constraint.nonroot="true" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="5s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="5000ms" sovereign.hft.cpu-pins="4-5" sovereign.hft.cpu-pins-mode="shared" sovereign.hft.deploy-strategy="standard-rolling" sovereign.hft.pre-stop-hook="true" sovereign.hft.pre-stop-delay="5s" sovereign.hft.connection-drain="true" sovereign.hft.sched-policy="SCHED_OTHER" sovereign.hft.runtime="c"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["/opt/nxlog/bin/nxlog"]

CMD ["-c", "/app/conf/nxlog.conf"]
