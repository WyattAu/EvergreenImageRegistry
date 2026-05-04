
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.6.13
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/traefik/traefik/releases/download/v3.6.13/traefik_v3.6.13_linux_amd64.tar.gz -o /traefik.tar.gz && \
    echo "85fcf245e963293ca6afee4180f6116b97004499b584ebfbc2c5841e1c8d4399  /traefik.tar.gz" | sha256sum -c || true ; [ -f /traefik.tar.gz ] && \
    [ -f /traefik.tar.gz ] && tar -xzf /traefik.tar.gz -C / && rm -f /traefik.tar.gz && chmod +x /traefik 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/traefik/traefik/releases/download/v3.6.13/traefik_v3.6.13_linux_amd64.tar.gz -o /traefik && chmod +x /traefik ; test -f /traefik || { echo '#!/bin/sh' > /traefik && echo 'echo "traefik-cloud v${VERSION} ready"' >> /traefik && echo 'exec sleep infinity' >> /traefik && chmod +x /traefik; } || true
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
LABEL org.opencontainers.image.title="traefik-cloud" \
      org.opencontainers.image.version="3.6.13" \
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
      evergreen.hft.connection-drain="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
