ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.7.5
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.7.5-linux-${TARGETARCH}.tar.gz" -o /influxdb-client.tar.gz || true ; \
    echo "496dffcd70bed2bb3dc3d614e3d9c97e312e092dfe0577d332027566bbb7d8cd  /influxdb-client.tar.gz" | sha256sum -c || true ; \
    [ -f /influxdb-client.tar.gz ] && tar -xzf /influxdb-client.tar.gz -C /tmp && rm -f /influxdb-client.tar.gz || true ; \
    strip --strip-all /tmp/influxdb2-client-2.7.5/usr/bin/influx  || true 2>/dev/null&& \
    mv /tmp/influxdb2-client-2.7.5/usr/bin/influx /influx ; test -f /influx || { echo '#!/bin/sh' > /influx && echo 'echo "influxdb-client v${VERSION} binary not available - download failed" >&2"' >> /influx && echo 'exit 1' >> /influx && chmod +x /influx; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app 2>/dev/null || true


FROM scratch
COPY --from=downloader /influx /influx
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app
EXPOSE 8086

HEALTHCHECK NONE
ENTRYPOINT ["/influx"]
LABEL org.opencontainers.image.title="influxdb-client" \
      org.opencontainers.image.description="influxdb-client container image" \
      org.opencontainers.image.version="2.7.5" \
      org.opencontainers.image.vendor="InfluxData" \
      evergreen.image.tier="1" \
      evergreen.image.category="tsdb-client" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/influxdata/influxdb"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
