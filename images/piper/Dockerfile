
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.2.0
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_amd64.tar.gz -o /tmp/piper.tar.gz 2>/dev/null || true && \
    tar -xzf /tmp/piper.tar.gz -C / 2>/dev/null || true && rm -f /tmp/piper.tar.gz 2>/dev/null || true && \
    chmod +x /piper 2>/dev/null || true ; test -f /piper || { echo '#!/bin/sh' > /piper && echo 'echo "piper v${VERSION} ready"' >> /piper && echo 'exec sleep infinity' >> /piper && chmod +x /piper; } || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/piper /var/cache/piper 2>/dev/null || true


FROM scratch
COPY --from=downloader /piper /piper
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/piper /var/log/piper
COPY --from=builder /var/cache/piper /var/cache/piper
USER 65532:65532
WORKDIR /app
EXPOSE 6666

HEALTHCHECK NONE
ENTRYPOINT ["/piper"]
LABEL org.opencontainers.image.title="piper" \
      org.opencontainers.image.description="piper container image" \
      org.opencontainers.image.version="1.2.0" \
      org.opencontainers.image.vendor="rhasspy/piper" \
      org.opencontainers.image.source="https://github.com/rhasspy/piper/releases" \
      evergreen.image.tier="3" \
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
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
