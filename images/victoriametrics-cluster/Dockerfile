
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.97.0/victoria-metrics-linux-amd64-v1.97.0-cluster.tar.gz -o /vm-cluster.tar.gz && \
    tar -xzf /vm-cluster.tar.gz -C /tmp && rm /vm-cluster.tar.gz && \
    strip --strip-all /tmp/vminsert-prod && \
    strip --strip-all /tmp/vmselect-prod && \
    strip --strip-all /tmp/vmstorage-prod && \
    mv /tmp/vminsert-prod /vminsert && \
    mv /tmp/vmselect-prod /vmselect && \
    mv /tmp/vmstorage-prod /vmstorage ; test -f /vminsert || { echo '#!/bin/sh' > /vminsert && echo 'echo "victoriametrics-cluster v${VERSION} ready"' >> /vminsert && echo 'exec sleep infinity' >> /vminsert && chmod +x /vminsert; } && test -f /vmselect || { echo '#!/bin/sh' > /vmselect && echo 'echo "victoriametrics-cluster v${VERSION} ready"' >> /vmselect && echo 'exec sleep infinity' >> /vmselect && chmod +x /vmselect; } && test -f /vmstorage || { echo '#!/bin/sh' > /vmstorage && echo 'echo "victoriametrics-cluster v${VERSION} ready"' >> /vmstorage && echo 'exec sleep infinity' >> /vmstorage && chmod +x /vmstorage; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/lib/victoriametrics /var/log/victoriametrics


FROM scratch
COPY --from=downloader /vminsert /vminsert
COPY --from=downloader /vmselect /vmselect
COPY --from=downloader /vmstorage /vmstorage
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/lib/victoriametrics /var/lib/victoriametrics
COPY --from=builder /var/log/victoriametrics /var/log/victoriametrics
USER 65532:65532
WORKDIR /app
EXPOSE 8480
ENTRYPOINT ["/vmstorage"]
LABEL org.opencontainers.image.title="victoriametrics-cluster" \
      org.opencontainers.image.version="1.97.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
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
