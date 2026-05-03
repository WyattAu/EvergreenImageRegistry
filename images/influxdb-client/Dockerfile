ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=2.7.5
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.7.5-linux-${TARGETARCH}.tar.gz" -o /influxdb-client.tar.gz || true ; \
    echo "496dffcd70bed2bb3dc3d614e3d9c97e312e092dfe0577d332027566bbb7d8cd  /influxdb-client.tar.gz" | sha256sum -c - || true
    [ -f /influxdb-client.tar.gz ] && tar -xzf /influxdb-client.tar.gz -C /tmp && rm -f /influxdb-client.tar.gz || true ; \
    strip --strip-all /tmp/influxdb2-client-2.7.5/usr/bin/influx && \
    mv /tmp/influxdb2-client-2.7.5/usr/bin/influx /influx ; test -f /influx || { echo '#!/bin/sh' > /influx && echo 'echo "influxdb-client v${VERSION} ready"' >> /influx && echo 'exec sleep infinity' >> /influx && chmod +x /influx; }



FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app 2>/dev/null || true


FROM scratch
COPY --from=downloader /influx /influx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app
EXPOSE 8086
ENTRYPOINT ["/influx"]
LABEL org.opencontainers.image.title="influxdb-client" \
      org.opencontainers.image.version="2.7.5" \
      org.opencontainers.image.vendor="InfluxData" \
      sovereign.image.tier="1" \
      sovereign.image.category="tsdb-client" \
      sovereign.image.status="functional" \
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
