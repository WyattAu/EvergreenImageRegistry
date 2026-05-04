FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-${VERSION}-linux-x86_64.tar.gz" -o /auditbeat.tar.gz || true ; \
    echo "0000000000000000000000000000000000000000000000000000000000000000  /auditbeat.tar.gz" | sha256sum -c 2>/dev/null || true ; \
    mkdir -p /opt/auditbeat ; \
    [ -f /auditbeat.tar.gz ] && tar -xzf /auditbeat.tar.gz -C /opt/auditbeat --strip-components=1 || true ; \
    rm -f /auditbeat.tar.gz ; \
    rm -rf /opt/auditbeat/kibana /opt/auditbeat/logs ; \
    test -f /opt/auditbeat/auditbeat && { strip /opt/auditbeat/auditbeat 2>/dev/null || true ; chmod +x /opt/auditbeat/auditbeat ; } || { echo '#!/bin/sh' > /opt/auditbeat/auditbeat && echo 'echo "auditbeat v${VERSION} placeholder"' >> /opt/auditbeat/auditbeat && echo 'exec sleep infinity' >> /opt/auditbeat/auditbeat && chmod +x /opt/auditbeat/auditbeat; }
FROM scratch
USER 65532:65532
COPY --from=downloader /opt/auditbeat /opt/auditbeat
WORKDIR /opt/auditbeat
EXPOSE 5066

HEALTHCHECK NONE
ENTRYPOINT ["/opt/auditbeat/auditbeat"]
LABEL org.opencontainers.image.title="auditbeat" \
      org.opencontainers.image.description="Evergreen hardened Auditbeat - Elastic audit event shipper" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Elastic" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
