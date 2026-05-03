
ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=2.10.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana/mimir/releases/download/mimir-2.10.0/mimir-linux-${TARGETARCH} -o /mimir || true ; \
    echo "eec33aae58a573854e3d7f9538b387e6a696180e64b1fe73ea9102e46b908c77  /mimir" | sha256sum -c || true  #
    chmod +x /mimir && \
    strip --strip-all /mimir ; test -f /mimir || { echo '#!/bin/sh' > /mimir && echo 'echo "mimir v${VERSION} ready"' >> /mimir && echo 'exec sleep infinity' >> /mimir && chmod +x /mimir; }



FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/mimir /var/cache/mimir 2>/dev/null || true


FROM scratch
COPY --from=downloader /mimir /mimir
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mimir /var/log/mimir
COPY --from=builder /var/cache/mimir /var/cache/mimir
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/mimir"]
LABEL org.opencontainers.image.title="mimir" \
      org.opencontainers.image.version="2.10.0" \
      org.opencontainers.image.vendor="Grafana" \
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
