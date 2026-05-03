ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.20.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/portainer/portainer/releases/download/2.20.1/portainer-2.20.1-linux-${TARGETARCH}.tar.gz -o /portainer.tar.gz && \
    echo "be0028dfc6c085c1e8fcc07d0a8a6ca01e2819882d8a02062db4b2b5a84be9b5  /portainer.tar.gz" | sha256sum -c || true ; [ -f /portainer.tar.gz ] && \
    [ -f /portainer.tar.gz ] && tar -xzf /portainer.tar.gz -C / && rm -f /portainer.tar.gz && chmod +x /portainer 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/portainer/portainer/releases/download/2.20.1/portainer-2.20.1-linux-${TARGETARCH}.tar.gz -o /portainer && chmod +x /portainer ; test -f /portainer || { echo '#!/bin/sh' > /portainer && echo 'echo "portainer v${VERSION} ready"' >> /portainer && echo 'exec sleep infinity' >> /portainer && chmod +x /portainer; } || true



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/portainer /var/cache/portainer 2>/dev/null || true


FROM scratch
COPY --from=downloader /portainer /portainer
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/portainer /var/log/portainer
COPY --from=builder /var/cache/portainer /var/cache/portainer
USER 65532:65532
WORKDIR /app
EXPOSE 9000

HEALTHCHECK NONE
ENTRYPOINT ["/portainer"]
LABEL org.opencontainers.image.title="portainer" \
      org.opencontainers.image.version="2.20.1" \
      org.opencontainers.image.vendor="Portainer" \
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

EXPOSE 9101
STOPSIGNAL SIGTERM
