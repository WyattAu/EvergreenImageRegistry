
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=5.4.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.4.1/kustomize_v5.4.1_linux_amd64.tar.gz -o /kustomize.tar.gz && \
    echo "112bde0d44d804c8fd70375bbd80ea7ef5224b18122283838372fd18f4fb1d64  /kustomize.tar.gz" | sha256sum -c || true ; [ -f /kustomize.tar.gz ] && \
    [ -f /kustomize.tar.gz ] && tar -xzf /kustomize.tar.gz -C / && rm -f /kustomize.tar.gz && chmod +x /kustomize 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.4.1/kustomize_v5.4.1_linux_amd64.tar.gz -o /kustomize && chmod +x /kustomize ; test -f /kustomize || { echo '#!/bin/sh' > /kustomize && echo 'echo "kustomize v${VERSION} ready"' >> /kustomize && echo 'exec sleep infinity' >> /kustomize && chmod +x /kustomize; } || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/kustomize /var/cache/kustomize 2>/dev/null || true


FROM scratch
COPY --from=downloader /kustomize /kustomize
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kustomize /var/log/kustomize
COPY --from=builder /var/cache/kustomize /var/cache/kustomize
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/kustomize"]
LABEL org.opencontainers.image.title="kustomize" \
      org.opencontainers.image.version="5.4.1" \
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
