ARG VERSION=v1.5
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

# NOTE: Upstream image digest not pinned - update @sha256:... when stable digest is available
FROM ghcr.io/gethomepage/homepage:v1.5 AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/homepage /var/cache/homepage 2>/dev/null || true


FROM scratch
COPY --from=upstream /app /app
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/homepage /var/log/homepage
COPY --from=builder /var/cache/homepage /var/cache/homepage

WORKDIR /app

EXPOSE 3000
EXPOSE 9101

LABEL org.opencontainers.image.title="homepage" org.opencontainers.image.description="Homepage - Application dashboard" org.opencontainers.image.vendor="benphelps" org.opencontainers.image.source="https://github.com/benphelps/homepage" evergreen.image.tier="3" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="v1.5"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/app/homepage"]
