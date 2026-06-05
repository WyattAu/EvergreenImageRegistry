ARG VERSION=v1.13.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM ghcr.io/gethomepage/homepage:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/homepage-config /var/cache/homepage-config 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=upstream /app /app
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/homepage-config /var/log/homepage-config
COPY --from=builder /var/cache/homepage-config /var/cache/homepage-config

WORKDIR /app

EXPOSE 3000
EXPOSE 9101

LABEL org.opencontainers.image.title="homepage-config" org.opencontainers.image.description="Homepage - config mode" org.opencontainers.image.vendor="benphelps" org.opencontainers.image.source="https://github.com/benphelps/homepage" evergreen.image.tier="3" evergreen.constraint.nonroot="true" evergreen.base.image="scratch" \
      org.opencontainers.image.version="latest"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:3000"]

ENTRYPOINT ["/shim", "run"]

CMD ["-c", "homepage", "--", "--config", "/app/config"]
