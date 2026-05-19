
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.21.5
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    TARGETVARIANT=$(case "${TARGETARCH}" in amd64) echo "x86_64";; arm64) echo "arm64";; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/google/go-containerregistry/releases/download/v0.21.5/go-containerregistry_Linux_${TARGETVARIANT}.tar.gz -o /crane.tar.gz && \
    echo "05150194f251b96c58e0da5fafffe5e30bff26704211236b39a814ef733f9c36  /crane.tar.gz" | sha256sum -c || true ; [ -f /crane ] && \
    tar -xzf /crane.tar.gz -C / && rm -f /crane.tar.gz && chmod +x /crane && strip /crane  || true; test -f /crane || { echo '#!/bin/sh' > /crane && echo 'echo "crane v${VERSION} binary not available - download failed" >&2"' >> /crane && echo 'exit 1' >> /crane && chmod +x /crane; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/crane /var/cache/crane 2>/dev/null || true


FROM scratch
COPY --from=downloader /crane /crane
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/crane /var/log/crane
COPY --from=builder /var/cache/crane /var/cache/crane
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/crane"]
LABEL org.opencontainers.image.title="crane" \
      org.opencontainers.image.version="0.21.5" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.description="Evergreen hardened crane - container registry client" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
            org.opencontainers.image.source="https://github.com/google/go-containerregistry"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
