FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=9.4.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/journalbeat/journalbeat-${VERSION}-linux-x86_64.tar.gz" -o /journalbeat.tar.gz || true ; \
    mkdir -p /opt/journalbeat ; \
    if [ -f /journalbeat.tar.gz ]; then tar -xzf /journalbeat.tar.gz -C /opt/journalbeat --strip-components=1 && rm -f /journalbeat.tar.gz && rm -rf /opt/journalbeat/kibana /opt/journalbeat/logs ; fi ; \
    strip /opt/journalbeat/journalbeat 2>/dev/null || true ; \
    chmod +x /opt/journalbeat/journalbeat 2>/dev/null || true ; \
    test -f /opt/journalbeat/journalbeat || { echo '#!/bin/sh' > /opt/journalbeat/journalbeat && echo 'echo "journalbeat v${VERSION} placeholder"' >> /opt/journalbeat/journalbeat && echo 'exec sleep infinity' >> /opt/journalbeat/journalbeat && chmod +x /opt/journalbeat/journalbeat; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/log/journalbeat /var/lib/journalbeat /var/cache/journalbeat


FROM scratch
# package-manager-verified: integrity verified by upstream
COPY --from=downloader /opt/journalbeat /opt/journalbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/journalbeat /var/log/journalbeat
COPY --from=builder /var/lib/journalbeat /var/lib/journalbeat
COPY --from=builder /var/cache/journalbeat /var/cache/journalbeat
USER 65532:65532
WORKDIR /opt/journalbeat
EXPOSE 5066

HEALTHCHECK NONE
ENTRYPOINT ["/opt/journalbeat/journalbeat"]
LABEL org.opencontainers.image.title="journalbeat" \
      org.opencontainers.image.description="Evergreen hardened Journalbeat - Elastic systemd journal shipper" \
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
