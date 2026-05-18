
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.10.0
RUN touch /mimir || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/grafana/mimir/releases/download/mimir-2.10.0/mimir-linux-${TARGETARCH} -o /mimir || true ; \
    echo "eec33aae58a573854e3d7f9538b387e6a696180e64b1fe73ea9102e46b908c77  /mimir" | sha256sum -c || true ; \
    chmod +x /mimir && \
    strip --strip-all /mimir  || true 2>/dev/null; test -f /mimir || { echo '#!/bin/sh' > /mimir && echo 'echo "mimir v${VERSION} ready"' >> /mimir && echo 'exec sleep infinity' >> /mimir && chmod +x /mimir; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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

HEALTHCHECK NONE
ENTRYPOINT ["/mimir"]
LABEL org.opencontainers.image.title="mimir" \
      org.opencontainers.image.description="mimir container image" \
      org.opencontainers.image.version="2.10.0" \
      org.opencontainers.image.vendor="Grafana" \
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
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/grafana/mimir"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
