ARG VERSION=v1.43.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    buildah \
    ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app /var/log/buildah /var/cache/buildah /var/lib/containers 2>/dev/null || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates containers-common || true
COPY --from=builder /usr/bin/buildah /usr/local/bin/buildah
COPY --from=builder /app /app
COPY --from=builder /var/log/buildah /var/log/buildah
COPY --from=builder /var/cache/buildah /var/cache/buildah
RUN mkdir -p /var/lib/containers /run/containers 2>/dev/null || true && \
    adduser -u 65532 -D buildah 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["buildah"]
LABEL org.opencontainers.image.title="buildah" \
      org.opencontainers.image.description="Evergreen hardened buildah - OCI image builder" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
            org.opencontainers.image.source="https://github.com/containers/buildah" \
                  org.opencontainers.image.version="latest"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
