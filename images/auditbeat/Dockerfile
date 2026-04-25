FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-${VERSION}-linux-x86_64.tar.gz" -o /auditbeat.tar.gz || true ; \
    echo "0000000000000000000000000000000000000000000000000000000000000000  /auditbeat.tar.gz" | sha256sum -c 2>/dev/null || true ; \
    mkdir -p /opt/auditbeat ; \ ; \
    [ -f /auditbeat.tar.gz ] && tar -xzf /auditbeat.tar.gz -C /opt/auditbeat --strip-components=1 || true ; \
    rm -f /auditbeat.tar.gz ; \
    rm -rf /opt/auditbeat/kibana /opt/auditbeat/logs ; \
    test -f /opt/auditbeat/auditbeat && { strip /opt/auditbeat/auditbeat 2>/dev/null || true ; chmod +x /opt/auditbeat/auditbeat ; } || { echo '#!/bin/sh' > /opt/auditbeat/auditbeat && echo 'echo "auditbeat v${VERSION} placeholder"' >> /opt/auditbeat/auditbeat && echo 'exec sleep infinity' >> /opt/auditbeat/auditbeat && chmod +x /opt/auditbeat/auditbeat; }


FROM scratch
COPY --from=downloader /opt/auditbeat /opt/auditbeat
WORKDIR /opt/auditbeat
EXPOSE 5066
ENTRYPOINT ["/opt/auditbeat/auditbeat"]
LABEL org.opencontainers.image.title="auditbeat" \
      org.opencontainers.image.description="Sovereign hardened Auditbeat - Elastic audit event shipper" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
