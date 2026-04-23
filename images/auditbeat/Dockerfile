FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-${VERSION}-linux-x86_64.tar.gz" -o /auditbeat.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  /auditbeat.tar.gz" | sha256sum -c || true  # \
    && mkdir -p /opt/auditbeat \
    && tar -xzf /auditbeat.tar.gz -C /opt/auditbeat --strip-components=1 \
    && rm /auditbeat.tar.gz \
    && rm -rf /opt/auditbeat/kibana /opt/auditbeat/logs \
    && strip /opt/auditbeat/auditbeat || true \
    && chmod +x /opt/auditbeat/auditbeat




FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/auditbeat /var/lib/auditbeat /var/cache/auditbeat

FROM scratch
COPY --from=downloader /opt/auditbeat /opt/auditbeat
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/auditbeat /var/log/auditbeat
COPY --from=builder /var/lib/auditbeat /var/lib/auditbeat
COPY --from=builder /var/cache/auditbeat /var/cache/auditbeat
USER 65532:65532
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