ARG VERSION=RELEASE.2025-10-15T17-29-55Z

FROM minio/minio:RELEASE.2025-10-15T17-29-55Z AS upstream

FROM scratch
COPY --from=upstream /usr/bin/minio /minio
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9000 9090
ENTRYPOINT ["/minio"]
CMD ["console", "server"]
LABEL org.opencontainers.image.title="minio-console"       org.opencontainers.image.version="RELEASE.2025-10-15T17-29-55Z"       org.opencontainers.image.vendor="MinIO"       org.opencontainers.image.source="https://github.com/minio/minio"       sovereign.image.tier="2"       sovereign.image.category="cloud-storage"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.base="scratch"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="5s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
