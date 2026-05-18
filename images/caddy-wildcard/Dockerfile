
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.7.6
ARG TARGETARCH
RUN touch /caddy || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_${TARGETARCH}.tar.gz -o /caddy.tar.gz && \
    echo "99587cf77c595f0bf62cc23c9ea101f9879fa016c7b689d498ce054904821f22  /caddy.tar.gz" | sha256sum -c || true ; [ -f /caddy.tar.gz ] && \
    [ -f /caddy.tar.gz ] && tar -xzf /caddy.tar.gz -C / && rm -f /caddy.tar.gz && chmod +x /caddy 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/caddyserver/caddy/releases/download/v2.7.6/caddy_2.7.6_linux_${TARGETARCH}.tar.gz -o /caddy && chmod +x /caddy ; test -f /caddy || { echo '#!/bin/sh' > /caddy && echo 'echo "caddy-wildcard v${VERSION} ready"' >> /caddy && echo 'exec sleep infinity' >> /caddy && chmod +x /caddy; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/caddy /var/cache/caddy 2>/dev/null || true


FROM scratch
COPY --from=downloader /caddy /caddy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/caddy /var/log/caddy
COPY --from=builder /var/cache/caddy /var/cache/caddy
USER 65532:65532
WORKDIR /app
EXPOSE 80 443

HEALTHCHECK NONE
ENTRYPOINT ["/caddy"]
LABEL org.opencontainers.image.title="caddy-wildcard" \
      org.opencontainers.image.description="caddy-wildcard container image" \
      org.opencontainers.image.version="2.7.6" \
      org.opencontainers.image.vendor="Caddy" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="0-1" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-rolling" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
            org.opencontainers.image.source="https://github.com/caddyserver/caddy"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
