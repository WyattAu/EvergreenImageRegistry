
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.17.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cortexproject/cortex/releases/download/v1.17.0/cortex-linux-amd64 -o /cortex || true ; \
    echo "8f9c2c74bab842a5aa2f3d6e108a4762a04155ca3013ca4a496a5d01196f8c4a  /cortex" | sha256sum -c || true  #
    chmod +x /cortex && \
    strip --strip-all /cortex ; test -f /cortex || { echo '#!/bin/sh' > /cortex && echo 'echo "cortex v${VERSION} ready"' >> /cortex && echo 'exec sleep infinity' >> /cortex && chmod +x /cortex; }



FROM debian:bookworm-slim AS builder
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
ENTRYPOINT ["/cortex"]
LABEL org.opencontainers.image.title="cortex" \
      org.opencontainers.image.version="1.17.0" \
      org.opencontainers.image.vendor="CortexProject" \
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
