ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.58.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/oliver006/redis_exporter/releases/download/v1.58.0/redis_exporter-v1.58.0.linux-${TARGETARCH}.tar.gz -o /valkey-exporter.tar.gz && \
    echo "c982d4a083ba31b13adc7256792968438b995117b362f7c0cf895b6c577d2899  /valkey-exporter.tar.gz" | sha256sum -c ; [ -f /valkey-exporter.tar.gz ] && \
    [ -f /valkey-exporter.tar.gz ] && tar -xzf /valkey-exporter.tar.gz -C / && rm -f /valkey-exporter.tar.gz && chmod +x /redis_exporter 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/oliver006/redis_exporter/releases/download/v1.58.0/redis_exporter-v1.58.0.linux-${TARGETARCH}.tar.gz -o /valkey-exporter && chmod +x /valkey-exporterbinary not available - download failed" >&2"' >> /redis_exporter && echo 'exit 1' >> /redis_exporter && chmod +x /redis_exporter; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/valkey-exporter /var/cache/valkey-exporter 2>/dev/null || true


FROM scratch
COPY --from=downloader /redis_exporter /valkey-exporter
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/valkey-exporter /var/log/valkey-exporter
COPY --from=builder /var/cache/valkey-exporter /var/cache/valkey-exporter
USER 65532:65532
WORKDIR /app
EXPOSE 9121

HEALTHCHECK NONE
ENTRYPOINT ["/valkey-exporter"]
LABEL org.opencontainers.image.title="valkey-exporter" \
      org.opencontainers.image.version="1.58.0" \
      org.opencontainers.image.description="Valkey/Redis Prometheus Exporter" \
      org.opencontainers.image.vendor="oliver006" \
      org.opencontainers.image.source="https://github.com/oliver006/redis_exporter" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
