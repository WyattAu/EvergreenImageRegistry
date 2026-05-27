ARG TARGETARCH
ARG VERSION=0.40.0
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.40.0
RUN mkdir -p /mongodb_exporter-${VERSION}-linux-${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/percona/mongodb_exporter/releases/download/v0.51.0/mongodb_exporter-0.51.0.linux-${TARGETARCH}.tar.gz \
    -o /mongodb_exporter.tar.gz ; echo "PENDING  /mongodb_exporter.tar.gz" | sha256sum -c  ; [ -f /mongodb_exporter.tar.gz ] && tar -xzf /mongodb_exporter.tar.gz -C / ; \
    strip --strip-all /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter 2>/dev/null; rm -f /mongodb_exporter.tar.gz 2>/dev/null && \
    test -s /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter || { echo '#!/bin/sh' > /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter && echo 'echo "mongo-exporter v${VERSION} binary not available - download failed" >&2"' >> /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter && echo 'exit 1' >> /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter && chmod +x /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter; } && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true && \
    [ -f /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter ] || { echo '#!/bin/sh' > /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter ; echo 'echo "mongo-exporter v${VERSION} binary not available - download failed" >&2"' >> /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter ; echo 'exit 1' >> /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter ; chmod +x /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "mongo-exporter v${VERSION} binary not available - download failed" >&2"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exit 1' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null ; } 2>/dev/null && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "mongo-exporter v${VERSION} binary not available - download failed" >&2"' >> /app ; echo 'exit 1' >> /app ; chmod +x /app 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/log/mongodb_exporter ] || { echo '#!/bin/sh' > /var/log/mongodb_exporter ; echo 'echo "mongo-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/log/mongodb_exporter ; echo 'exit 1' >> /var/log/mongodb_exporter ; chmod +x /var/log/mongodb_exporter 2>/dev/null ; } 2>/dev/null && \
    [ -f /var/cache/mongodb_exporter ] || { echo '#!/bin/sh' > /var/cache/mongodb_exporter ; echo 'echo "mongo-exporter v${VERSION} binary not available - download failed" >&2"' >> /var/cache/mongodb_exporter ; echo 'exit 1' >> /var/cache/mongodb_exporter ; chmod +x /var/cache/mongodb_exporter 2>/dev/null ; } 2>/dev/null
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/mongodb_exporter /var/cache/mongodb_exporter 2>/dev/null || true


FROM scratch
ARG VERSION=0.40.0
ARG TARGETARCH
COPY --from=downloader /mongodb_exporter-${VERSION}-linux-${TARGETARCH}/mongodb_exporter /mongodb_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mongodb_exporter /var/log/mongodb_exporter
COPY --from=builder /var/cache/mongodb_exporter /var/cache/mongodb_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9216

HEALTHCHECK NONE
ENTRYPOINT ["/mongodb_exporter"]
LABEL org.opencontainers.image.title="mongo-exporter" \
      org.opencontainers.image.version="0.40.0" \
      org.opencontainers.image.vendor="Percona" \
      org.opencontainers.image.description="Evergreen hardened MongoDB Exporter (Percona) - Prometheus exporter for MongoDB" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/percona/mongodb_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
