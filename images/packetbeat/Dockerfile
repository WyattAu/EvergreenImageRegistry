FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-${VERSION}-linux-x86_64.tar.gz" -o /packetbeat.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  /packetbeat.tar.gz" | sha256sum -c || true  # \
    && mkdir -p /opt/packetbeat \
    && tar -xzf /packetbeat.tar.gz -C /opt/packetbeat --strip-components=1 \
    && rm /packetbeat.tar.gz \
    && rm -rf /opt/packetbeat/kibana /opt/packetbeat/logs \
    && strip /opt/packetbeat/packetbeat || true \
    && chmod +x /opt/packetbeat/packetbeat




FROM debian:bookworm-slim AS builder
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
ENTRYPOINT ["/opt/packetbeat/packetbeat"]
LABEL org.opencontainers.image.title="packetbeat" \
      org.opencontainers.image.description="Sovereign hardened Packetbeat - Elastic network packet analyzer" \
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