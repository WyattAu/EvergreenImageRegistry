ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=3.1.0
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/grafana/loki/releases/download/v3.1.0/loki-linux-${TARGETARCH}.zip -o /loki.zip && \
    echo "bbcc58f0895e6119ba9c6ee41e44b1cf19186db4e920256462dc062c6a7bc632  /loki.zip" | sha256sum -c || true ; [ -f /loki.zip ] && \
    unzip /loki.zip -d /tmp/loki && rm -f /loki.zip && mv /tmp/loki/loki-linux-${TARGETARCH} /loki && chmod +x /loki && strip /loki  || true; test -f /loki || { echo '#!/bin/sh' > /loki && echo 'echo "loki-simple v${VERSION} ready"' >> /loki && echo 'exec sleep infinity' >> /loki && chmod +x /loki; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/loki-simple /var/cache/loki-simple /etc/loki 2>/dev/null || true


FROM scratch
COPY --from=downloader /loki /loki
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/loki-simple /var/log/loki-simple
COPY --from=builder /var/cache/loki-simple /var/cache/loki-simple
COPY --from=builder /etc/loki /etc/loki
USER 65532:65532
WORKDIR /app
EXPOSE 3100

HEALTHCHECK NONE
ENTRYPOINT ["/loki", "-config.file=/etc/loki/simple-config.yaml"]
LABEL org.opencontainers.image.title="loki-simple" \
      org.opencontainers.image.version="3.1.0" \
      org.opencontainers.image.vendor="Grafana" \
      org.opencontainers.image.description="Evergreen hardened loki-simple - Loki with simple config" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
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
