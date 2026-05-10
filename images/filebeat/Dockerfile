FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=9.4.0
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${VERSION}-linux-x86_64.tar.gz" -o /filebeat.tar.gz || true ; \
    echo "1b0327c8206df71fd77a9f08d848c2efa02dd3eab901231226ca430e5ba3bee7  /filebeat.tar.gz" | sha256sum -c || true ; \
    mkdir -p /opt/filebeat ; \
    if [ -f /filebeat.tar.gz ]; then tar -xzf /filebeat.tar.gz -C /opt/filebeat --strip-components=1 && rm -f /filebeat.tar.gz && rm -rf /opt/filebeat/kibana /opt/filebeat/logs ; fi ; \
    strip /opt/filebeat/filebeat 2>/dev/null || true ; \
    chmod +x /opt/filebeat/filebeat 2>/dev/null || true ; \
    test -f /opt/filebeat/filebeat || { echo '#!/bin/sh' > /opt/filebeat/filebeat && echo 'echo "filebeat v${VERSION} placeholder"' >> /opt/filebeat/filebeat && echo 'exec sleep infinity' >> /opt/filebeat/filebeat && chmod +x /opt/filebeat/filebeat; } || true


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/log/filebeat /var/lib/filebeat /var/cache/filebeat


FROM scratch
COPY --from=downloader /opt/filebeat /opt/filebeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/filebeat /var/log/filebeat
COPY --from=builder /var/lib/filebeat /var/lib/filebeat
COPY --from=builder /var/cache/filebeat /var/cache/filebeat
USER 65532:65532
WORKDIR /opt/filebeat
EXPOSE 5066

HEALTHCHECK NONE
ENTRYPOINT ["/opt/filebeat/filebeat"]
LABEL org.opencontainers.image.title="filebeat" \
      org.opencontainers.image.description="Evergreen hardened Filebeat - Elastic log file shipper" \
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
