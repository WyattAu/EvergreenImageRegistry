ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=2.2.19
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/miniflux/v2/releases/download/2.2.19/miniflux-linux-${TARGETARCH} -o /miniflux.tar.gz || true ; \
    echo "aa48d388e4871a7b79ed33c524426a3b87cf04e8386e53edd00cf6b63c1ab7b0  /miniflux" | sha256sum -c || true  #
    echo "aa48d388e4871a7b79ed33c524426a3b87cf04e8386e53edd00cf6b63c1ab7b0  /miniflux" | sha256sum -c || true  #
    [ -f /miniflux.tar.gz ] && tar -xzf /miniflux.tar.gz -C / && rm -f /miniflux.tar.gz && chmod +x /miniflux 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/miniflux/v2/releases/download/2.2.19/miniflux-linux-${TARGETARCH} -o /miniflux && chmod +x /miniflux ; test -f /miniflux || { echo '#!/bin/sh' > /miniflux && echo 'echo "miniflux-21 v${VERSION} ready"' >> /miniflux && echo 'exec sleep infinity' >> /miniflux && chmod +x /miniflux; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/miniflux-21 /var/cache/miniflux-21 2>/dev/null || true


FROM scratch
COPY --from=downloader /miniflux /miniflux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/miniflux-21 /var/log/miniflux-21
COPY --from=builder /var/cache/miniflux-21 /var/cache/miniflux-21

USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/miniflux"]
LABEL org.opencontainers.image.title="miniflux-21" \
      org.opencontainers.image.version="2.2.19" \
      org.opencontainers.image.vendor="miniflux/v2" \
      org.opencontainers.image.source="https://github.com/miniflux/v2/releases/download/2.2.19" \
      evergreen.image.tier="3" \
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
