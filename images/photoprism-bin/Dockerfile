FROM debian:bookworm-slim AS downloader
ARG VERSION=260305-fad9d5395
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://github.com/photoprism/photoprism/releases/download/${VERSION}/photoprism_${VERSION}-linux-amd64.tar.gz" \
    -o /tmp/photoprism.tar.gz && \
    tar -xzf /tmp/photoprism.tar.gz -C /tmp/ && \
    cp /tmp/photoprism /photoprism && chmod +x /photoprism && \
    rm -rf /tmp/photoprism.tar.gz /tmp/photoprism

FROM scratch
COPY --from=downloader /photoprism /photoprism
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 2282
ENTRYPOINT ["/photoprism"]
LABEL org.opencontainers.image.title="photoprism-bin"       org.opencontainers.image.version="260305-fad9d5395"       org.opencontainers.image.vendor="PhotoPrism"       org.opencontainers.image.source="https://github.com/photoprism/photoprism"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"       sovereign.hft.signal-handling="native"       sovereign.hft.shutdown-timeout="3s"       sovereign.hft.init-system="none"       sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
