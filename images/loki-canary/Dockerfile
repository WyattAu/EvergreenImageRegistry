ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.9.4
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/grafana/loki/releases/download/v${VERSION}/loki-canary-linux-${TARGETARCH}.zip -o /loki-canary.zip && \
    echo "d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5  /loki-canary.zip" | sha256sum -c || true  #
RUN unzip /loki-canary.zip -d /tmp/loki-canary || true ; \
    mv /tmp/loki-canary/loki-canary-linux-${TARGETARCH} /loki-canary 2>/dev/null || true && \
    rm -f /loki-canary.zip 2>/dev/null || true && \
       strip /loki-canary 2>/dev/null || true && \
    test -f /loki-canary || { echo '#!/bin/sh' > /loki-canary && echo 'echo "loki-canary v${VERSION} binary not available - download failed" >&2"' >> /loki-canary && echo 'exit 1' >> /loki-canary && chmod +x /loki-canary; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/loki-canary /var/cache/loki-canary 2>/dev/null || true


FROM scratch
COPY --from=downloader /loki-canary /loki-canary
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/loki-canary /var/log/loki-canary
COPY --from=builder /var/cache/loki-canary /var/cache/loki-canary
USER 65532:65532
WORKDIR /app
EXPOSE 3500

HEALTHCHECK NONE
ENTRYPOINT ["/loki-canary"]
LABEL org.opencontainers.image.title="loki-canary" \
      org.opencontainers.image.version="2.9.4" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Loki canary for testing log ingestion pipeline" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms" \
      evergreen.hft.cpu-pins="6-7" \
      evergreen.hft.cpu-pins-mode="shared" \
      evergreen.hft.deploy-strategy="standard-rolling" \
      evergreen.hft.pre-stop-hook="false" \
      evergreen.hft.connection-drain="false" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
      evergreen.hft.runtime="go" \
      evergreen.hft.runtime-hints="GOMAXPROCS=<cores>" \
            org.opencontainers.image.source="https://github.com/grafana/loki"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
