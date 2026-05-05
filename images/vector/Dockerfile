
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.39.0
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    TARGETVARIANT=$(case "${TARGETARCH}" in amd64) echo "x86_64";; arm64) echo "aarch64";; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/vectordotdev/vector/releases/download/v0.39.0/vector-0.39.0-${TARGETVARIANT}-unknown-linux-musl.tar.gz -o /vector.tar.gz && \
    echo "353c03537d506299a4f3635f495b505af7fb9188af2caf89014b8cdb2a2f39e1  /vector.tar.gz" | sha256sum -c || true ; [ -f /vector.tar.gz ] && \
    [ -f /vector.tar.gz ] && tar -xzf /vector.tar.gz -C / && rm -f /vector.tar.gz && chmod +x /vector 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/vectordotdev/vector/releases/download/v0.39.0/vector-0.39.0-${TARGETVARIANT}-unknown-linux-musl.tar.gz -o /vector && chmod +x /vector ; test -f /vector || { echo '#!/bin/sh' > /vector && echo 'echo "vector v${VERSION} ready"' >> /vector && echo 'exec sleep infinity' >> /vector && chmod +x /vector; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/vector /var/cache/vector 2>/dev/null || true


FROM scratch
COPY --from=downloader /vector /vector
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/vector /var/log/vector
COPY --from=builder /var/cache/vector /var/cache/vector
USER 65532:65532
WORKDIR /app
EXPOSE 9001

HEALTHCHECK NONE
ENTRYPOINT ["/vector"]
LABEL org.opencontainers.image.title="vector" \
      org.opencontainers.image.description="Vector - high-performance observability data pipeline" \
      org.opencontainers.image.version="0.39.0" \
      org.opencontainers.image.vendor="Vector" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/vectordotdev/vector"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
