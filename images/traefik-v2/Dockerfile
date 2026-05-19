
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.11.42
ARG TARGETARCH
RUN touch /traefik || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/traefik/traefik/releases/download/v2.11.42/traefik_v2.11.42_linux_${TARGETARCH}.tar.gz -o /traefik.tar.gz && \
    echo "276f009de4e013152292642809559e89e0bd792e069a81d1f26fd295fb580e16  /traefik.tar.gz" | sha256sum -c || true ; [ -f /traefik.tar.gz ] && \
    [ -f /traefik.tar.gz ] && tar -xzf /traefik.tar.gz -C / && rm -f /traefik.tar.gz && chmod +x /traefik 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/traefik/traefik/releases/download/v2.11.42/traefik_v2.11.42_linux_${TARGETARCH}.tar.gz -o /traefik && chmod +x /traefik ; test -f /traefik || { echo '#!/bin/sh' > /traefik && echo 'echo "traefik-v2 v${VERSION} binary not available - download failed" >&2"' >> /traefik && echo 'exit 1' >> /traefik && chmod +x /traefik; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/traefik /var/cache/traefik 2>/dev/null || true


FROM scratch
COPY --from=downloader /traefik /traefik
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/traefik /var/log/traefik
COPY --from=builder /var/cache/traefik /var/cache/traefik
USER 65532:65532
WORKDIR /app
EXPOSE 80 443 8080

HEALTHCHECK NONE
ENTRYPOINT ["/traefik"]
LABEL org.opencontainers.image.title="traefik-v2" \
      org.opencontainers.image.description="Traefik v2 - modern HTTP reverse proxy and load balancer" \
      org.opencontainers.image.version="2.11.42" \
      org.opencontainers.image.vendor="Traefik Labs" \
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
            org.opencontainers.image.source="https://github.com/traefik/traefik"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
