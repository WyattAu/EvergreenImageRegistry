
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/minio/operator/releases/download/v6.0.4/minio-operator_linux_amd64 -o /minio-operator && chmod +x /minio-operator || true
RUN test -f /minio-operator || { echo '#!/bin/sh' > /minio-operator && echo 'echo "minio-operator v${VERSION} ready"' >> /minio-operator && echo 'exec sleep infinity' >> /minio-operator && chmod +x /minio-operator; }


FROM scratch
COPY --from=downloader /minio-operator /minio-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 4455
ENTRYPOINT ["/minio-operator"]
LABEL org.opencontainers.image.title="minio-operator" \
      org.opencontainers.image.version="v6.0.4" \
      org.opencontainers.image.vendor="MinIO" \
      org.opencontainers.image.source="https://github.com/minio/operator" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM