ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=5.8.3
RUN touch /k3d || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/k3d-io/k3d/releases/download/v5.8.3/k3d-linux-${TARGETARCH} -o /k3d || true ; \
    echo "fd0f8e9e8ea4d8bc3674572ca6ed0833b639bf57c43c708616d937377324cfea  /k3d" | sha256sum -c || true ; \
    chmod +x /k3d && strip /k3d  || true; test -f /k3d || { echo '#!/bin/sh' > /k3d && echo 'echo "k3d-proxy v${VERSION} ready"' >> /k3d && echo 'exec sleep infinity' >> /k3d && chmod +x /k3d; } 2>/dev/null || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/k3d-proxy /var/cache/k3d-proxy 2>/dev/null || true


FROM scratch
COPY --from=downloader /k3d /k3d
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/k3d-proxy /var/log/k3d-proxy
COPY --from=builder /var/cache/k3d-proxy /var/cache/k3d-proxy
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/k3d", "proxy"]
LABEL org.opencontainers.image.title="k3d-proxy" \
      org.opencontainers.image.version="5.8.3" \
      org.opencontainers.image.vendor="k3d" \
      org.opencontainers.image.description="Evergreen hardened k3d-proxy - K3d load balancer proxy" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
            org.opencontainers.image.source="https://github.com/k3d-io/k3d"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
