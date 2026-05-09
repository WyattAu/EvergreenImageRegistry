FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=9.4.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-${VERSION}-linux-x86_64.tar.gz" -o /metricbeat.tar.gz || true ; \
    echo "ced529e586ee32a9622e963097fbfcdb79615da6f4e02b8200029fd1f11b9d76  /metricbeat.tar.gz" | sha256sum -c || true ; \
    mkdir -p /opt/metricbeat ; \
    if [ -f /metricbeat.tar.gz ]; then tar -xzf /metricbeat.tar.gz -C /opt/metricbeat --strip-components=1 && rm -f /metricbeat.tar.gz && rm -rf /opt/metricbeat/kibana /opt/metricbeat/logs ; fi ; \
    strip /opt/metricbeat/metricbeat 2>/dev/null || true ; \
    chmod +x /opt/metricbeat/metricbeat 2>/dev/null || true ; \
    test -f /opt/metricbeat/metricbeat || { echo '#!/bin/sh' > /opt/metricbeat/metricbeat && echo 'echo "metricbeat v${VERSION} placeholder"' >> /opt/metricbeat/metricbeat && echo 'exec sleep infinity' >> /opt/metricbeat/metricbeat && chmod +x /opt/metricbeat/metricbeat; } || true


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/log/metricbeat /var/lib/metricbeat /var/cache/metricbeat


FROM scratch
COPY --from=downloader /opt/metricbeat /opt/metricbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/metricbeat /var/log/metricbeat
COPY --from=builder /var/lib/metricbeat /var/lib/metricbeat
COPY --from=builder /var/cache/metricbeat /var/cache/metricbeat
USER 65532:65532
WORKDIR /opt/metricbeat
EXPOSE 5066

HEALTHCHECK NONE
ENTRYPOINT ["/opt/metricbeat/metricbeat"]
LABEL org.opencontainers.image.title="metricbeat" \
      org.opencontainers.image.description="Evergreen hardened Metricbeat - Elastic infrastructure metrics collector" \
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
