ARG VERSION=v0.4
ARG TARGETARCH

FROM mickaelkerjean/filestash@sha256:cf0edfe1ebcc164ebc7b8b88b9135018764800198a3606f2f9a62334f5d1f2c9 AS upstream

FROM scratch
COPY --from=upstream /app/filestash /filestash
COPY --from=upstream /app/dist /dist
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8334

HEALTHCHECK NONE
ENTRYPOINT ["/filestash"]
LABEL org.opencontainers.image.title="filestash" \
      org.opencontainers.image.description="filestash container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Filestash" \
      org.opencontainers.image.source="https://github.com/mickael-kerjean/filestash" \
      evergreen.image.tier="2" \
      evergreen.image.category="cloud-storage" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
