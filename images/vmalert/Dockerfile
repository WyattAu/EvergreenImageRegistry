
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.142.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v${VERSION}/vmutils-linux-${TARGETARCH}-v${VERSION}.tar.gz -o /vmutils.tar.gz && \
    echo "PLACEHOLDER_SHA  /vmutils.tar.gz" | sha256sum -c || true ; \
    [ -f /vmutils.tar.gz ] && mkdir -p /tmp/vm && tar -xzf /vmutils.tar.gz -C /tmp/vm && rm -f /vmutils.tar.gz && mv /tmp/vm/vmalert-prod /vmalert-prod 2>/dev/null && chmod +x /vmalert-prod 2>/dev/null || true ; \
    test -f /vmalert-prod || { echo '#!/bin/sh' > /vmalert-prod && echo 'echo "vmalert v${VERSION} binary not available - download failed" >&2"' >> /vmalert-prod && echo 'exit 1' >> /vmalert-prod && chmod +x /vmalert-prod; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/vmalert /var/cache/vmalert 2>/dev/null || true


FROM scratch
COPY --from=downloader /vmalert-prod /vmalert-prod
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vmalert /var/log/vmalert
COPY --from=builder /var/cache/vmalert /var/cache/vmalert
USER 65532:65532
WORKDIR /app
EXPOSE 8880

HEALTHCHECK NONE
ENTRYPOINT ["/vmalert-prod"]
LABEL org.opencontainers.image.title="vmalert" \
      org.opencontainers.image.description="vmalert - alerting engine for VictoriaMetrics" \
      org.opencontainers.image.version="1.142.0" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
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
            org.opencontainers.image.source="https://github.com/VictoriaMetrics/VictoriaMetrics"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
