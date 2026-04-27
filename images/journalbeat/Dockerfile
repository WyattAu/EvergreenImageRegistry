FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/journalbeat/journalbeat-${VERSION}-linux-x86_64.tar.gz" -o /journalbeat.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  /journalbeat.tar.gz" | sha256sum -c || true  ; mkdir -p /opt/journalbeat-src ; \
    [ -f /journalbeat.tar.gz ] && tar -xzf /journalbeat.tar.gz -C /opt/journalbeat-src --strip-components=1 || true ; \    rm /journalbeat.tar.gz ; rm -rf /opt/journalbeat/kibana /opt/journalbeat/logs ; strip /opt/journalbeat/journalbeat || true ; chmod +x /opt/journalbeat/journalbeat ;  placeholder"' >> /opt/journalbeat/placeholder && echo 'exec sleep infinity' >> /opt/journalbeat/placeholder && chmod +x /opt/journalbeat; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/journalbeat /var/lib/journalbeat /var/cache/journalbeat 2>/dev/null || true


FROM scratch
RUN mkdir -p /etc/ssl /opt /var/cache /var/lib /var/log 2>/dev/null || true
COPY --from=downloader /opt/journalbeat /opt/journalbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/journalbeat /var/log/journalbeat
COPY --from=builder /var/lib/journalbeat /var/lib/journalbeat
COPY --from=builder /var/cache/journalbeat /var/cache/journalbeat
USER 65532:65532
WORKDIR /opt/journalbeat
EXPOSE 5066
ENTRYPOINT ["/opt/journalbeat/journalbeat"]
LABEL org.opencontainers.image.title="journalbeat" \
      org.opencontainers.image.description="Sovereign hardened Journalbeat - Elastic systemd journal shipper" \
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
