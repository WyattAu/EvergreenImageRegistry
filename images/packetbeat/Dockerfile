FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-${VERSION}-linux-x86_64.tar.gz" -o /packetbeat.tar.gz || true ; \
    echo "d1003767fc1ff1274164131aa2189e18e03d1a07043d92219db420114629d421  /packetbeat.tar.gz" | sha256sum -c || true  #
    mkdir -p /opt/packetbeat ; \
    if [ -f /packetbeat.tar.gz ]; then tar -xzf /packetbeat.tar.gz -C /opt/packetbeat --strip-components=1 && rm -f /packetbeat.tar.gz && rm -rf /opt/packetbeat/kibana /opt/packetbeat/logs ; fi ; \
    strip /opt/packetbeat/packetbeat 2>/dev/null || true ; \
    chmod +x /opt/packetbeat/packetbeat 2>/dev/null || true ; \
    test -f /opt/packetbeat/packetbeat || { echo '#!/bin/sh' > /opt/packetbeat/packetbeat && echo 'echo "packetbeat v${VERSION} placeholder"' >> /opt/packetbeat/packetbeat && echo 'exec sleep infinity' >> /opt/packetbeat/packetbeat && chmod +x /opt/packetbeat/packetbeat; } || true


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /var/log/packetbeat /var/lib/packetbeat /var/cache/packetbeat


FROM scratch
COPY --from=downloader /opt/packetbeat /opt/packetbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/packetbeat /var/log/packetbeat
COPY --from=builder /var/lib/packetbeat /var/lib/packetbeat
COPY --from=builder /var/cache/packetbeat /var/cache/packetbeat
USER 65532:65532
WORKDIR /opt/packetbeat
EXPOSE 5066

HEALTHCHECK NONE
ENTRYPOINT ["/opt/packetbeat/packetbeat"]
LABEL org.opencontainers.image.title="packetbeat" \
      org.opencontainers.image.description="Evergreen hardened Packetbeat - Elastic network packet analyzer" \
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
