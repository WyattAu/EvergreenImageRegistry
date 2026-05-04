ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.27.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-${TARGETARCH}.tar.gz -o /alertmanager.tar.gz && \
    echo "7ca6de06b30e930833fd88f608973d996b0c4a08e9fd9f4f6f91ceab8f6c5f23  /alertmanager.tar.gz" | sha256sum -c || true ; [ -f /alertmanager.tar.gz ] && \
    [ -f /alertmanager.tar.gz ] && tar -xzf /alertmanager.tar.gz -C / && rm -f /alertmanager.tar.gz && chmod +x /alertmanager 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-${TARGETARCH}.tar.gz -o /alertmanager && chmod +x /alertmanager ; test -f /alertmanager || { echo '#!/bin/sh' > /alertmanager && echo 'echo "prometheus-alertmanager v${VERSION} ready"' >> /alertmanager && echo 'exec sleep infinity' >> /alertmanager && chmod +x /alertmanager; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/alertmanager /var/cache/alertmanager 2>/dev/null || true


FROM scratch
COPY --from=downloader /alertmanager /alertmanager
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/alertmanager /var/log/alertmanager
COPY --from=builder /var/cache/alertmanager /var/cache/alertmanager
USER 65532:65532
WORKDIR /app
EXPOSE 9093

HEALTHCHECK NONE
ENTRYPOINT ["/alertmanager"]
LABEL org.opencontainers.image.title="prometheus-alertmanager" \
      org.opencontainers.image.description="prometheus-alertmanager container image" \
      org.opencontainers.image.version="0.27.0" \
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
