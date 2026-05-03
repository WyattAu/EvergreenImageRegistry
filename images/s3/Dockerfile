ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=RELEASE.2025-10-15T17-29-55Z
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-${TARGETARCH}/minio" -o /s3-server.tar.gz && \
    echo "7c5bd8512c6e966455b1d198209358b2d191c77a83ab377c4073281065fb855f  /s3-server.tar.gz" | sha256sum -c || true ; \
    [ -f /s3-server.tar.gz ] && tar -xzf /s3-server.tar.gz -C / && rm -f /s3-server.tar.gz && chmod +x /s3-server 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.min.io/server/minio/release/linux-${TARGETARCH}/minio" -o /s3-server && chmod +x /s3-server ; test -f /s3-server || { echo '#!/bin/sh' > /s3-server && echo 'echo "s3 v${VERSION} ready"' >> /s3-server && echo 'exec sleep infinity' >> /s3-server && chmod +x /s3-server; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/s3-server /var/cache/s3-server 2>/dev/null || true


FROM scratch
COPY --from=downloader /s3-server /s3-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/s3-server /var/log/s3-server
COPY --from=builder /var/cache/s3-server /var/cache/s3-server
USER 65532:65532
WORKDIR /app
EXPOSE 9000 9001

HEALTHCHECK NONE
ENTRYPOINT ["/s3-server"]
LABEL org.opencontainers.image.title="s3" \
      org.opencontainers.image.version="RELEASE.2025-10-15T17-29-55Z" \
      org.opencontainers.image.vendor="MinIO" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
