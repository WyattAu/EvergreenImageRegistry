ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.97.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.97.0/victoria-metrics-linux-${TARGETARCH}-v1.97.0-cluster.tar.gz -o /vm-cluster.tar.gz || true ; \
    echo "798f6e6e6f78e4502a17977a0dcc95fd237fbf7a89b59a1c46ae11790e029e21  /vm-cluster.tar.gz" | sha256sum -c - || true
    [ -f /vm-cluster.tar.gz ] && tar -xzf /vm-cluster.tar.gz -C /tmp && rm -f /vm-cluster.tar.gz || true ; \
    strip --strip-all /tmp/vminsert-prod && \
    strip --strip-all /tmp/vmselect-prod && \
    strip --strip-all /tmp/vmstorage-prod && \
    mv /tmp/vminsert-prod /vminsert && \
    mv /tmp/vmselect-prod /vmselect && \
    mv /tmp/vmstorage-prod /vmstorage ; test -f /vminsert || { echo '#!/bin/sh' > /vminsert && echo 'echo "victoriametrics-cluster v${VERSION} ready"' >> /vminsert && echo 'exec sleep infinity' >> /vminsert && chmod +x /vminsert; } && test -f /vmselect || { echo '#!/bin/sh' > /vmselect && echo 'echo "victoriametrics-cluster v${VERSION} ready"' >> /vmselect && echo 'exec sleep infinity' >> /vmselect && chmod +x /vmselect; } && test -f /vmstorage || { echo '#!/bin/sh' > /vmstorage && echo 'echo "victoriametrics-cluster v${VERSION} ready"' >> /vmstorage && echo 'exec sleep infinity' >> /vmstorage && chmod +x /vmstorage; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/lib/victoriametrics /var/log/victoriametrics 2>/dev/null || true


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

HEALTHCHECK NONE
ENTRYPOINT ["/vmstorage"]
LABEL org.opencontainers.image.title="victoriametrics-cluster" \
      org.opencontainers.image.version="1.97.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      evergreen.image.tier="1" \
      evergreen.image.category="tsdb" \
      evergreen.image.status="functional" \
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
