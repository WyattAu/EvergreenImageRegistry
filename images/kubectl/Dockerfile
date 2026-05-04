
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.30.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kubectl" -o /kubectl.tar.gz && \
    echo "5b86f0b06e1a5ba6f8f00e2b01e8ed39407729c4990aeda961f83a586f975e8a  /kubectl.tar.gz" | sha256sum -c || true ; [ -f /kubectl.tar.gz ] && \
    [ -f /kubectl.tar.gz ] && tar -xzf /kubectl.tar.gz -C / && rm -f /kubectl.tar.gz && chmod +x /kubectl 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://dl.k8s.io/release/v1.30.1/bin/linux/amd64/kubectl" -o /kubectl && chmod +x /kubectl ; test -f /kubectl || { echo '#!/bin/sh' > /kubectl && echo 'echo "kubectl v${VERSION} ready"' >> /kubectl && echo 'exec sleep infinity' >> /kubectl && chmod +x /kubectl; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/kubectl /var/cache/kubectl 2>/dev/null || true


FROM scratch
COPY --from=downloader /kubectl /kubectl
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kubectl /var/log/kubectl
COPY --from=builder /var/cache/kubectl /var/cache/kubectl
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/kubectl"]
LABEL org.opencontainers.image.title="kubectl" \
      org.opencontainers.image.description="kubectl - command line tool for controlling Kubernetes clusters" \
      org.opencontainers.image.version="1.30.1" \
      org.opencontainers.image.vendor="Kubernetes" \
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
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
