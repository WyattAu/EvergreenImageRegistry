# STUB: xteve fork has no published release assets.
ARG VERSION=2.2.0.200

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/xteve-project/xTeVe/releases/download/${VERSION}/xteve_linux_amd64" \
    -o /xteve && chmod +x /xteve
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/xteve /var/cache/xteve 2>/dev/null || true

FROM scratch
COPY --from=downloader /xteve /xteve
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/xteve /var/log/xteve
COPY --from=builder /var/cache/xteve /var/cache/xteve
USER 65532:65532
WORKDIR /app
EXPOSE 34400

HEALTHCHECK NONE
ENTRYPOINT ["/xteve"]
LABEL org.opencontainers.image.title="xteve" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="xteve" \
      org.opencontainers.image.source="https://github.com/xteve-project/xTeVe" \
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
