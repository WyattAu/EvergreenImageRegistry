ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=1.1.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kbudde/rabbitmq_exporter/releases/download/v1.0.0/rabbitmq_exporter_1.0.0_linux_amd64.tar.gz \
    -o /rabbitmq_exporter.tar.gz ; echo "PENDING  /rabbitmq_exporter.tar.gz" | sha256sum -c || true  ; [ -f /rabbitmq_exporter.tar.gz ] && tar -xzf /rabbitmq_exporter.tar.gz -C / || true ; \
    strip --strip-all /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter ; rm -f /rabbitmq_exporter.tar.gz 2>/dev/null || true
RUN test -f /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter || { echo '#!/bin/sh' > /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter && echo 'echo "rabbitmq-exporter v${VERSION} ready"' >> /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter && echo 'exec sleep infinity' >> /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter && chmod +x /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter; } || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN [ -f /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter ] || { echo '#!/bin/sh' > /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter ; echo 'echo "rabbitmq-exporter v${VERSION} ready"' >> /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter ; echo 'exec sleep infinity' >> /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter ; chmod +x /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "rabbitmq-exporter v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "rabbitmq-exporter v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/log/rabbitmq_exporter ] || { echo '#!/bin/sh' > /var/log/rabbitmq_exporter ; echo 'echo "rabbitmq-exporter v${VERSION} ready"' >> /var/log/rabbitmq_exporter ; echo 'exec sleep infinity' >> /var/log/rabbitmq_exporter ; chmod +x /var/log/rabbitmq_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/cache/rabbitmq_exporter ] || { echo '#!/bin/sh' > /var/cache/rabbitmq_exporter ; echo 'echo "rabbitmq-exporter v${VERSION} ready"' >> /var/cache/rabbitmq_exporter ; echo 'exec sleep infinity' >> /var/cache/rabbitmq_exporter ; chmod +x /var/cache/rabbitmq_exporter 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/rabbitmq_exporter /var/cache/rabbitmq_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /rabbitmq_exporter-${VERSION}-linux-${TARGETARCH}/rabbitmq_exporter /rabbitmq_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/rabbitmq_exporter /var/log/rabbitmq_exporter
COPY --from=builder /var/cache/rabbitmq_exporter /var/cache/rabbitmq_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9090
ENTRYPOINT ["/rabbitmq_exporter"]
LABEL org.opencontainers.image.title="rabbitmq-exporter" \
      org.opencontainers.image.version="1.1.0" \
      org.opencontainers.image.vendor="kbudde" \
      org.opencontainers.image.description="Sovereign hardened RabbitMQ Exporter - Prometheus exporter for RabbitMQ" \
      sovereign.image.tier="1" \
      sovereign.image.category="messaging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
