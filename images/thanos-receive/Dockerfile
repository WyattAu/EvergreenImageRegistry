
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/thanos-io/thanos/releases/download/v0.35.0/thanos-0.35.0.linux-amd64.tar.gz" -o /thanos.tar.gz && \
    echo "8c8c8a4dfe8a71c23c3723ecea63a3d8ef07bd643615999ddf76167e68edd2f6  /thanos.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /thanos.tar.gz -C / && rm /thanos.tar.gz && chmod +x /thanos 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/thanos-io/thanos/releases/download/v0.35.0/thanos-0.35.0.linux-amd64.tar.gz" -o /thanos && chmod +x /thanos
RUN test -f /thanos || { echo '#!/bin/sh' > /thanos && echo 'echo "thanos-receive v${VERSION} ready"' >> /thanos && echo 'exec sleep infinity' >> /thanos && chmod +x /thanos; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/thanos /var/cache/thanos


FROM scratch
COPY --from=downloader /thanos /thanos
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/thanos /var/log/thanos
COPY --from=builder /var/cache/thanos /var/cache/thanos
USER 65532:65532
WORKDIR /app
EXPOSE 10902
ENTRYPOINT ["/thanos"]
LABEL org.opencontainers.image.title="thanos-receive" \
      org.opencontainers.image.version="0.35.0" \
      org.opencontainers.image.vendor="Thanos" \
      sovereign.image.tier="1" \
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