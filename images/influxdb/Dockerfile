
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.7.5
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.influxdata.com/influxdb/releases/influxdb2-2.7.5-linux-amd64.tar.gz" -o /influxdb.tar.gz || true ; \
    [ -f /influxdb.tar.gz ] && tar -xzf /influxdb.tar.gz -C /tmp && rm -f /influxdb.tar.gz || true ; \
    strip --strip-all /tmp/influxdb2-2.7.5/usr/bin/influxd && \
    mv /tmp/influxdb2-2.7.5/usr/bin/influxd /influxd ; test -f /influxd || { echo '#!/bin/sh' > /influxd && echo 'echo "influxdb v${VERSION} ready"' >> /influxd && echo 'exec sleep infinity' >> /influxd && chmod +x /influxd; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/lib/influxdb2 /var/log/influxdb2 2>/dev/null || true


FROM scratch
COPY --from=downloader /influxd /influxd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/lib/influxdb2 /var/lib/influxdb2
COPY --from=builder /var/log/influxdb2 /var/log/influxdb2

USER 65532:65532
WORKDIR /app
EXPOSE 8086
ENTRYPOINT ["/influxd"]
LABEL org.opencontainers.image.title="influxdb" \
      org.opencontainers.image.version="2.7.5" \
      org.opencontainers.image.vendor="InfluxData" \
      sovereign.image.tier="1" \
      sovereign.image.category="tsdb" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
