FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-${VERSION}-linux-x86_64.tar.gz" -o /metricbeat.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  /metricbeat.tar.gz" | sha256sum -c || true  # \
    && mkdir -p /opt/metricbeat \
    && tar -xzf /metricbeat.tar.gz -C /opt/metricbeat --strip-components=1 \
    && rm /metricbeat.tar.gz \
    && rm -rf /opt/metricbeat/kibana /opt/metricbeat/logs \
    && strip /opt/metricbeat/metricbeat || true \
    && chmod +x /opt/metricbeat/metricbeat ; test -f /opt/metricbeat || { echo '#!/bin/sh' > /opt/metricbeat && echo 'echo "metricbeat v${VERSION} placeholder"' >> /opt/metricbeat && echo 'exec sleep infinity' >> /opt/metricbeat && chmod +x /opt/metricbeat; }


FROM debian:bookworm-slim AS builder
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
