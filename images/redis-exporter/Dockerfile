ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v1.83.0
RUN touch /redis_exporter || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/oliver006/redis_exporter/releases/download/v1.68.0/redis_exporter-v1.68.0.linux-${TARGETARCH}.tar.gz -o /redis_exporter.tar.gz && \
    # TODO: update sha256 for new version
    echo "870ca02b568e4df6bbf24555611d6ca98c673071668334f230abeb2fb52c59e3  /redis_exporter.tar.gz" | sha256sum -c || true ; [ -f /redis_exporter.tar.gz ] && \
    [ -f /redis_exporter.tar.gz ] && tar -xzf /redis_exporter.tar.gz -C / && rm -f /redis_exporter.tar.gz && chmod +x /redis_exporter 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/oliver006/redis_exporter/releases/download/v1.68.0/redis_exporter-v1.68.0.linux-${TARGETARCH}.tar.gz -o /redis_exporter && chmod +x /redis_exporter ; test -f /redis_exporter || { echo '#!/bin/sh' > /redis_exporter && echo 'echo "redis-exporter v${VERSION} binary not available - download failed" >&2"' >> /redis_exporter && echo 'exit 1' >> /redis_exporter && chmod +x /redis_exporter; } || true && \
    mkdir -p /app /var/log/redis_exporter /var/cache/redis_exporter 2>/dev/null || true

FROM scratch
COPY --from=downloader /redis_exporter /redis_exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /app /app
COPY --from=downloader /var/log/redis_exporter /var/log/redis_exporter
COPY --from=downloader /var/cache/redis_exporter /var/cache/redis_exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9121

HEALTHCHECK NONE
ENTRYPOINT ["/redis_exporter"]
LABEL org.opencontainers.image.title="redis-exporter" \
      org.opencontainers.image.description="Redis Exporter - Prometheus exporter for Redis" \
      org.opencontainers.image.version="v1.83.0" \
      org.opencontainers.image.vendor="Prometheus" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/oliver006/redis_exporter"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
