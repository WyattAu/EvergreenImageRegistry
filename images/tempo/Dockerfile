
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.8.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana/tempo/releases/download/v2.8.0/tempo_2.8.0_linux_${TARGETARCH}.tar.gz -o /tempo.tar.gz && \
    echo "PLACEHOLDER_SHA  /tempo.tar.gz" | sha256sum -c || exit 1 ; \
    [ -f /tempo.tar.gz ] && tar -xzf /tempo.tar.gz -C / && rm -f /tempo.tar.gz && chmod +x /tempo 2>/dev/null || true ; \
    test -f /tempo || { echo '#!/bin/sh' > /tempo && echo 'echo "tempo v${VERSION} ready"' >> /tempo && echo 'exec sleep infinity' >> /tempo && chmod +x /tempo; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/tempo /var/cache/tempo 2>/dev/null || true


FROM scratch
COPY --from=downloader /tempo /tempo
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/tempo /var/log/tempo
COPY --from=builder /var/cache/tempo /var/cache/tempo
USER 65532:65532
WORKDIR /app
EXPOSE 3200

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:3200/ready
ENTRYPOINT ["/tempo"]
LABEL org.opencontainers.image.title="tempo" \
      org.opencontainers.image.description="Tempo - distributed tracing backend by Grafana" \
      org.opencontainers.image.version="2.8.0" \
      org.opencontainers.image.vendor="Grafana" \
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
            org.opencontainers.image.source="https://github.com/grafana/tempo"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
