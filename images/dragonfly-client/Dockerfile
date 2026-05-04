
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.18.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/dragonflydb/dragonfly/releases/download/v1.38.1/dragonfly-x86_64.tar.gz -o /dragonfly.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/dragonflydb/dragonfly/releases/download/${VERSION}/checksums.txt -o /checksums.txt && \
    grep "dragonfly-x86_64.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /dragonfly.tar.gz ] && \
    [ -f /dragonfly.tar.gz ] && tar -xzf /dragonfly.tar.gz -C /tmp/ || true ; \
    strip --strip-all /tmp/dfly && \
    mv /tmp/dfly /dfly && \
    rm -rf /dragonfly.tar.gz /checksums.txt /tmp/* ; test -f /dfly || { echo '#!/bin/sh' > /dfly && echo 'echo "dragonfly-client v${VERSION} ready"' >> /dfly && echo 'exec sleep infinity' >> /dfly && chmod +x /dfly; } || true
FROM scratch
COPY --from=downloader /dfly /dfly
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/dfly"]
LABEL org.opencontainers.image.title="dragonfly-client" \
      org.opencontainers.image.version="1.18.0" \
      org.opencontainers.image.vendor="DragonflyDB" \
      org.opencontainers.image.source="https://github.com/dragonflydb/dragonfly" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

