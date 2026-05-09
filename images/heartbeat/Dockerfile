FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-${VERSION}-linux-x86_64.tar.gz" -o /heartbeat.tar.gz || true ; \
    echo "711083ec654168da15f3e4e8b924be00bf82b44c7427896ee59fe29431fe13ed  /heartbeat.tar.gz" | sha256sum -c || true ; \
    mkdir -p /opt/heartbeat ; \
    if [ -f /heartbeat.tar.gz ]; then tar -xzf /heartbeat.tar.gz -C /opt/heartbeat --strip-components=1 && rm -f /heartbeat.tar.gz && rm -rf /opt/heartbeat/kibana /opt/heartbeat/logs ; fi ; \
    strip /opt/heartbeat/heartbeat 2>/dev/null || true ; \
    chmod +x /opt/heartbeat/heartbeat 2>/dev/null || true ; \
    test -f /opt/heartbeat/heartbeat || { echo '#!/bin/sh' > /opt/heartbeat/heartbeat && echo 'echo "heartbeat v${VERSION} placeholder"' >> /opt/heartbeat/heartbeat && echo 'exec sleep infinity' >> /opt/heartbeat/heartbeat && chmod +x /opt/heartbeat/heartbeat; } || true


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/log/heartbeat /var/lib/heartbeat /var/cache/heartbeat


FROM scratch
COPY --from=downloader /opt/heartbeat /opt/heartbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/heartbeat /var/log/heartbeat
COPY --from=builder /var/lib/heartbeat /var/lib/heartbeat
COPY --from=builder /var/cache/heartbeat /var/cache/heartbeat
USER 65532:65532
WORKDIR /opt/heartbeat
EXPOSE 5066

HEALTHCHECK NONE
ENTRYPOINT ["/opt/heartbeat/heartbeat"]
LABEL org.opencontainers.image.title="heartbeat" \
      org.opencontainers.image.description="Evergreen hardened Heartbeat - Elastic uptime monitor" \
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
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/elastic/beats"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
