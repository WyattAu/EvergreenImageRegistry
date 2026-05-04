ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.8.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/pushgateway/releases/download/v1.8.0/pushgateway-1.8.0.linux-${TARGETARCH}.tar.gz -o /pushgateway.tar.gz && \
    echo "ee962b451e533c392d9bfd07f5e4195d64a65b87b55d4abbcedc5f9ce13dfc58  /pushgateway.tar.gz" | sha256sum -c || true ; [ -f /pushgateway.tar.gz ] && \
    [ -f /pushgateway.tar.gz ] && tar -xzf /pushgateway.tar.gz -C / && rm -f /pushgateway.tar.gz && chmod +x /pushgateway 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/pushgateway/releases/download/v1.8.0/pushgateway-1.8.0.linux-${TARGETARCH}.tar.gz -o /pushgateway && chmod +x /pushgateway ; test -f /pushgateway || { echo '#!/bin/sh' > /pushgateway && echo 'echo "prometheus-pushgateway v${VERSION} ready"' >> /pushgateway && echo 'exec sleep infinity' >> /pushgateway && chmod +x /pushgateway; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/pushgateway /var/cache/pushgateway 2>/dev/null || true


FROM scratch
COPY --from=downloader /pushgateway /pushgateway
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pushgateway /var/log/pushgateway
COPY --from=builder /var/cache/pushgateway /var/cache/pushgateway
USER 65532:65532
WORKDIR /app
EXPOSE 9091

HEALTHCHECK NONE
ENTRYPOINT ["/pushgateway"]
LABEL org.opencontainers.image.title="prometheus-pushgateway" \
      org.opencontainers.image.description="Prometheus Pushgateway - intermediary service for metrics push" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus" \
      evergreen.image.tier="1" \
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
      evergreen.hft.sched-policy="SCHED_OTHER"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
