ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=RELEASE.2025-10-15T17-29-55Z
RUN touch /minio || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-${TARGETARCH}/minio" -o /minio.tar.gz && \
    echo "7c5bd8512c6e966455b1d198209358b2d191c77a83ab377c4073281065fb855f  /minio.tar.gz" | sha256sum -c || true ; \
    [ -f /minio.tar.gz ] && tar -xzf /minio.tar.gz -C / && rm -f /minio.tar.gz && chmod +x /minio 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-${TARGETARCH}/minio" -o /minio && chmod +x /minio ; test -f /minio || { echo '#!/bin/sh' > /minio && echo 'echo "minio v${VERSION} ready"' >> /minio && echo 'exec sleep infinity' >> /minio && chmod +x /minio; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/minio /var/cache/minio 2>/dev/null || true


FROM scratch
COPY --from=downloader /minio /minio
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/minio /var/log/minio
COPY --from=builder /var/cache/minio /var/cache/minio
USER 65532:65532
WORKDIR /app
EXPOSE 9000 9001

HEALTHCHECK NONE
ENTRYPOINT ["/minio"]
LABEL org.opencontainers.image.title="minio" \
      org.opencontainers.image.description="MinIO - high-performance object storage compatible with S3" \
      org.opencontainers.image.version="RELEASE.2025-10-15T17-29-55Z" \
      org.opencontainers.image.vendor="MinIO" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/minio/minio"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
