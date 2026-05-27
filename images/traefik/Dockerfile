
ARG TARGETARCH
ARG VERSION=v3.7.1
ARG APP_UID=65532
ARG APP_GID=65532
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=v3.7.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/traefik/traefik/releases/download/${VERSION}/traefik_${VERSION}_linux_${TARGETARCH}.tar.gz -o /traefik.tar.gz ; \
    [ -f /traefik.tar.gz ] && tar -xzf /traefik.tar.gz -C / && rm -f /traefik.tar.gz && chmod +x /traefik 2>/dev/null ; \binary not available - download failed" >&2"' >> /traefik && echo 'exit 1' >> /traefik && chmod +x /traefik; }


FROM scratch
ARG VERSION=v3.7.1
COPY --from=downloader /traefik /traefik
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 80 443 8080

HEALTHCHECK NONE
ENTRYPOINT ["/traefik"]
LABEL org.opencontainers.image.title="traefik" \
      org.opencontainers.image.description="Traefik - modern HTTP reverse proxy and load balancer" \
      org.opencontainers.image.version="v3.7.1" \
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
      evergreen.hft.xdp-capable="false" \
      evergreen.hft.xdp-notes="Not supported; use envoy for XDP workloads" \
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
