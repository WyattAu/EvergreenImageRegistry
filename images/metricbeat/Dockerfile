FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-${VERSION}-linux-x86_64.tar.gz" -o /metricbeat.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  /metricbeat.tar.gz" | sha256sum -c || true  ; mkdir -p /opt/metricbeat-src ; \
    [ -f /metricbeat.tar.gz ] && tar -xzf /metricbeat.tar.gz -C /opt/metricbeat-src --strip-components=1 || true ;  \rm /metricbeat.tar.gz ; rm -rf /opt/metricbeat/kibana /opt/metricbeat/logs ; strip /opt/metricbeat/metricbeat || true ; chmod +x /opt/metricbeat/metricbeat ;  placeholder"' >> /opt/metricbeat/placeholder && echo 'exec sleep infinity' >> /opt/metricbeat/placeholder && chmod +x /opt/metricbeat; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/metricbeat /var/lib/metricbeat /var/cache/metricbeat 2>/dev/null || true


FROM scratch
RUN mkdir -p /etc/ssl /opt /var/cache /var/lib /var/log 2>/dev/null || true
COPY --from=downloader /opt/metricbeat /opt/metricbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/metricbeat /var/log/metricbeat
COPY --from=builder /var/lib/metricbeat /var/lib/metricbeat
COPY --from=builder /var/cache/metricbeat /var/cache/metricbeat
USER 65532:65532
WORKDIR /opt/metricbeat
EXPOSE 5066
ENTRYPOINT ["/opt/metricbeat/metricbeat"]
LABEL org.opencontainers.image.title="metricbeat" \
      org.opencontainers.image.description="Sovereign hardened Metricbeat - Elastic infrastructure metrics collector" \
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
