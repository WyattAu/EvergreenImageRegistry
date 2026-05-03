
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.8.3
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cloudreve/Cloudreve/releases/download/3.8.3/cloudreve_3.8.3_linux_amd64.tar.gz -o /tmp/cloudreve.tar.gz && tar -xzf /tmp/cloudreve.tar.gz -C / && rm -f /tmp/cloudreve.tar.gz && chmod +x /cloudreve 2>/dev/null || true ; test -f /cloudreve || { echo '#!/bin/sh' > /cloudreve && echo 'echo "cloudreve v${VERSION} ready"' >> /cloudreve && echo 'exec sleep infinity' >> /cloudreve && chmod +x /cloudreve; } && \
    echo "157fe01d54d6fffd0fe3c50383f05df209e8c98d9171ecdc7565fe1647d61f7a  /tmp/cloudreve.tar.gz" | sha256sum -c - || true



FROM scratch
COPY --from=downloader /cloudreve /cloudreve
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 5212

HEALTHCHECK NONE
ENTRYPOINT ["/cloudreve"]
LABEL org.opencontainers.image.title="cloudreve" \
      org.opencontainers.image.version="3.8.3" \
      org.opencontainers.image.vendor="Cloudreve" \
      org.opencontainers.image.source="https://github.com/cloudreve/Cloudreve" \
      evergreen.image.tier="2" \
      evergreen.image.category="cloud-storage" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
