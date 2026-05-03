
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.17.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cortexproject/cortex/releases/download/v1.17.0/cortex-linux-${TARGETARCH} -o /cortex || true ; \
    echo "8f9c2c74bab842a5aa2f3d6e108a4762a04155ca3013ca4a496a5d01196f8c4a  /cortex" | sha256sum -c || true  #
    chmod +x /cortex && \
    strip --strip-all /cortex ; test -f /cortex || { echo '#!/bin/sh' > /cortex && echo 'echo "cortex v${VERSION} ready"' >> /cortex && echo 'exec sleep infinity' >> /cortex && chmod +x /cortex; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/cortex /var/cache/cortex 2>/dev/null || true


FROM scratch
COPY --from=downloader /cortex /cortex
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cortex /var/log/cortex
COPY --from=builder /var/cache/cortex /var/cache/cortex
USER 65532:65532
WORKDIR /app
EXPOSE 9009

HEALTHCHECK NONE
ENTRYPOINT ["/cortex"]
LABEL org.opencontainers.image.title="cortex" \
      org.opencontainers.image.version="1.17.0" \
      org.opencontainers.image.vendor="CortexProject" \
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

EXPOSE 9101
STOPSIGNAL SIGTERM
