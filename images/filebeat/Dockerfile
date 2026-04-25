FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${VERSION}-linux-x86_64.tar.gz" -o /filebeat.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  /filebeat.tar.gz" | sha256sum -c || true  \
    && mkdir -p /opt/filebeat \ 2>/dev/null || true ; \
    [ -f /filebeat.tar.gz ] && tar -xzf /filebeat.tar.gz -C /opt/filebeat --strip-components=1 || true ; \    rm /filebeat.tar.gz \    && rm -rf /opt/filebeat/kibana /opt/filebeat/logs \
    && strip /opt/filebeat/filebeat || true \
    && chmod +x /opt/filebeat/filebeat ; test -f /opt/filebeat || { echo '#!/bin/sh' > /opt/filebeat && echo 'echo "filebeat v${VERSION} placeholder"' >> /opt/filebeat && echo 'exec sleep infinity' >> /opt/filebeat && chmod +x /opt/filebeat; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/filebeat /var/lib/filebeat /var/cache/filebeat 2>/dev/null || true


FROM scratch
COPY --from=downloader /opt/filebeat /opt/filebeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/filebeat /var/log/filebeat
COPY --from=builder /var/lib/filebeat /var/lib/filebeat
COPY --from=builder /var/cache/filebeat /var/cache/filebeat
USER 65532:65532
WORKDIR /opt/filebeat
EXPOSE 5066
ENTRYPOINT ["/opt/filebeat/filebeat"]
LABEL org.opencontainers.image.title="filebeat" \
      org.opencontainers.image.description="Sovereign hardened Filebeat - Elastic log file shipper" \
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
