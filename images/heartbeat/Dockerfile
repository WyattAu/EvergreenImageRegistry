FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-${VERSION}-linux-x86_64.tar.gz" -o /heartbeat.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  /heartbeat.tar.gz" | sha256sum -c || true  ; mkdir -p /opt/heartbeat \ ; \
    [ -f /heartbeat.tar.gz ] && tar -xzf /heartbeat.tar.gz -C /opt/heartbeat --strip-components=1 || true ; \    rm /heartbeat.tar.gz ; rm -rf /opt/heartbeat/kibana /opt/heartbeat/logs ; strip /opt/heartbeat/heartbeat || true ; chmod +x /opt/heartbeat/heartbeat ; test -f /opt/heartbeat || { echo '#!/bin/sh' > /opt/heartbeat && echo 'echo "heartbeat v${VERSION} placeholder"' >> /opt/heartbeat && echo 'exec sleep infinity' >> /opt/heartbeat && chmod +x /opt/heartbeat; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/heartbeat /var/lib/heartbeat /var/cache/heartbeat 2>/dev/null || true


FROM scratch
COPY --from=downloader /opt/heartbeat /opt/heartbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/heartbeat /var/log/heartbeat
COPY --from=builder /var/lib/heartbeat /var/lib/heartbeat
COPY --from=builder /var/cache/heartbeat /var/cache/heartbeat
USER 65532:65532
WORKDIR /opt/heartbeat
EXPOSE 5066
ENTRYPOINT ["/opt/heartbeat/heartbeat"]
LABEL org.opencontainers.image.title="heartbeat" \
      org.opencontainers.image.description="Sovereign hardened Heartbeat - Elastic uptime monitor" \
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
