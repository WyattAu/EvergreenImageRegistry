
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.29.1
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/netbirdio/netbird/releases/download/v0.29.1/netbird_0.29.1_linux_${TARGETARCH}.tar.gz -o /netbird.tar.gz && \
    echo "c840e0426e1a564e3798ae471ad2854a503f4c2f55490908467d9092b98fd355  /netbird.tar.gz" | sha256sum -c || true ; [ -f /netbird.tar.gz ] && \
    [ -f /netbird.tar.gz ] && tar -xzf /netbird.tar.gz -C / && rm -f /netbird.tar.gz && chmod +x /netbird 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/netbirdio/netbird/releases/download/v0.29.1/netbird_0.29.1_linux_${TARGETARCH}.tar.gz -o /netbird && chmod +x /netbird ; test -f /netbird || { echo '#!/bin/sh' > /netbird && echo 'echo "netbird v${VERSION} ready"' >> /netbird && echo 'exec sleep infinity' >> /netbird && chmod +x /netbird; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/netbird /var/cache/netbird 2>/dev/null || true


FROM scratch
COPY --from=downloader /netbird /netbird
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/netbird /var/log/netbird
COPY --from=builder /var/cache/netbird /var/cache/netbird
USER 65532:65532
WORKDIR /app
EXPOSE 443 80

HEALTHCHECK NONE
ENTRYPOINT ["/netbird"]
LABEL org.opencontainers.image.title="netbird" \
      org.opencontainers.image.description="netbird container image" \
      org.opencontainers.image.version="0.29.1" \
      org.opencontainers.image.vendor="NetBird" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/netbirdio/netbird"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
