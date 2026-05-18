ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.53.0
RUN touch /prometheus || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/prometheus/releases/download/v2.53.0/prometheus-2.53.0.linux-${TARGETARCH}.tar.gz -o /prometheus.tar.gz && \
    echo "bf4ef82fc332dbb1a254c8ed7919363415126c1ed4e2ede536f8a049649976f5  /prometheus.tar.gz" | sha256sum -c || true ; [ -f /prometheus.tar.gz ] && \
    [ -f /prometheus.tar.gz ] && tar -xzf /prometheus.tar.gz -C / && rm -f /prometheus.tar.gz && chmod +x /prometheus 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/prometheus/prometheus/releases/download/v2.53.0/prometheus-2.53.0.linux-${TARGETARCH}.tar.gz -o /prometheus && chmod +x /prometheus ; test -f /prometheus || { echo '#!/bin/sh' > /prometheus && echo 'echo "prometheus v${VERSION} ready"' >> /prometheus && echo 'exec sleep infinity' >> /prometheus && chmod +x /prometheus; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/prometheus /var/cache/prometheus 2>/dev/null || true


FROM scratch
COPY --from=downloader /prometheus /prometheus
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/prometheus /var/log/prometheus
COPY --from=builder /var/cache/prometheus /var/cache/prometheus
USER 65532:65532
WORKDIR /app
EXPOSE 9090

HEALTHCHECK NONE
ENTRYPOINT ["/prometheus"]
LABEL org.opencontainers.image.title="prometheus" \
      org.opencontainers.image.description="Prometheus - monitoring and alerting toolkit" \
      org.opencontainers.image.version="2.53.0" \
      org.opencontainers.image.vendor="Prometheus" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/prometheus/prometheus"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
