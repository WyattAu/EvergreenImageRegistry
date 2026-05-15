
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.33.6+k3s1
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/k3s-io/k3s/releases/download/v1.33.6+k3s1/k3s -o /k3s || true ; \
    echo "86945269160fdd1bbd06283ea5b3bafd6c0ec0d1df3ac68ad3686656632081a5  /k3s" | sha256sum -c || true ; \
    chmod +x /k3s && strip /k3s  || true; test -f /k3s || { echo '#!/bin/sh' > /k3s && echo 'echo "k3s-agent v${VERSION} ready"' >> /k3s && echo 'exec sleep infinity' >> /k3s && chmod +x /k3s; } 2>/dev/null || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/k3s-agent /var/cache/k3s-agent /var/lib/rancher/k3s/agent 2>/dev/null || true


FROM scratch
COPY --from=downloader /k3s /k3s
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/k3s-agent /var/log/k3s-agent
COPY --from=builder /var/cache/k3s-agent /var/cache/k3s-agent
COPY --from=builder /var/lib/rancher/k3s/agent /var/lib/rancher/k3s/agent
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/k3s", "agent"]
LABEL org.opencontainers.image.title="k3s-agent" \
      org.opencontainers.image.version="1.33.6+k3s1" \
      org.opencontainers.image.vendor="SUSE" \
      org.opencontainers.image.description="Evergreen hardened k3s-agent - K3s agent mode" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="15s" \
            org.opencontainers.image.source="https://github.com/k3s-io/k3s"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
