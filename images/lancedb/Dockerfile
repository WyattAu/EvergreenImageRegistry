ARG VERSION=v0.21.0

FROM ghcr.io/lancedb/lancedb:v0.21.0 AS upstream

FROM scratch
# package-manager-verified: integrity verified by upstream
COPY --from=upstream /lancedb /lancedb
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN true
USER 65532:65532
WORKDIR /app
EXPOSE 6333

HEALTHCHECK NONE
ENTRYPOINT ["/lancedb"]
LABEL org.opencontainers.image.title="lancedb" \
      org.opencontainers.image.description="lancedb container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="lancedb/lance" \
      org.opencontainers.image.source="https://github.com/lancedb/lance" \
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
