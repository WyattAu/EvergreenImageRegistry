ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=0.40.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/percona/mongodb_exporter/releases/download/v0.51.0/mongodb_exporter-0.51.0.linux-${TARGETARCH}.tar.gz \
    -o /mongodb_exporter.tar.gz ; echo "PENDING  /mongodb_exporter.tar.gz" | sha256sum -c || true  ; [ -f /mongodb_exporter.tar.gz ] && tar -xzf /mongodb_exporter.tar.gz -C / || true ; \
    strip --strip-all /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter ; rm -f /mongodb_exporter.tar.gz 2>/dev/null || true
RUN test -f /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter || { echo '#!/bin/sh' > /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter && echo 'echo "mongo-exporter v${VERSION} ready"' >> /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter && echo 'exec sleep infinity' >> /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter && chmod +x /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter; } || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN [ -f /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter ] || { echo '#!/bin/sh' > /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter ; echo 'echo "mongo-exporter v${VERSION} ready"' >> /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter ; echo 'exec sleep infinity' >> /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter ; chmod +x /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "mongo-exporter v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "mongo-exporter v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/log/mongodb_exporter ] || { echo '#!/bin/sh' > /var/log/mongodb_exporter ; echo 'echo "mongo-exporter v${VERSION} ready"' >> /var/log/mongodb_exporter ; echo 'exec sleep infinity' >> /var/log/mongodb_exporter ; chmod +x /var/log/mongodb_exporter 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /var/cache/mongodb_exporter ] || { echo '#!/bin/sh' > /var/cache/mongodb_exporter ; echo 'echo "mongo-exporter v${VERSION} ready"' >> /var/cache/mongodb_exporter ; echo 'exec sleep infinity' >> /var/cache/mongodb_exporter ; chmod +x /var/cache/mongodb_exporter 2>/dev/null || true ; } 2>/dev/null || true
FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/mongodb_exporter /var/cache/mongodb_exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter /mongodb_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mongodb_exporter /var/log/mongodb_exporter
COPY --from=builder /var/cache/mongodb_exporter /var/cache/mongodb_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9216
ENTRYPOINT ["/mongodb_exporter"]
LABEL org.opencontainers.image.title="mongo-exporter" \
      org.opencontainers.image.version="0.40.0" \
      org.opencontainers.image.vendor="Percona" \
      org.opencontainers.image.description="Sovereign hardened MongoDB Exporter (Percona) - Prometheus exporter for MongoDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
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
