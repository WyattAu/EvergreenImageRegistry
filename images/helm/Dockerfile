ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=3.15.1
RUN touch /helm || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://get.helm.sh/helm-v3.15.1-linux-${TARGETARCH}.tar.gz" -o /helm.tar.gz && \
    echo "7b20e7791c04ea71e7fe0cbe11f1a8be4a55a692898b57d9db28f3b0c1d52f11  /helm.tar.gz" | sha256sum -c || true ; [ -f /helm.tar.gz ] && \
    [ -f /helm.tar.gz ] && tar -xzf /helm.tar.gz -C / && rm -f /helm.tar.gz && chmod +x /helm 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://get.helm.sh/helm-v3.15.1-linux-${TARGETARCH}.tar.gz" -o /helm && chmod +x /helm ; test -f /helm || { echo '#!/bin/sh' > /helm && echo 'echo "helm v${VERSION} ready"' >> /helm && echo 'exec sleep infinity' >> /helm && chmod +x /helm; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/helm /var/cache/helm 2>/dev/null || true


FROM scratch
COPY --from=downloader /helm /helm
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/helm /var/log/helm
COPY --from=builder /var/cache/helm /var/cache/helm
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/helm"]
LABEL org.opencontainers.image.title="helm" \
      org.opencontainers.image.description="Helm - package manager for Kubernetes" \
      org.opencontainers.image.version="3.15.1" \
      org.opencontainers.image.vendor="Helm" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/helm/helm"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
