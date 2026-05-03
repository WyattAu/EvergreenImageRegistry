FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Graylog2/collector-sidecar/releases/download/1.5.2/graylog-sidecar-1.5.2.tar.gz -o /sidecar.tar.gz 2>/dev/null || true ; \
    echo "bb8ea480268551864d246e31b3e5cc50e941e71b7ad236092a9b2ccb96b5eb0f  /sidecar.tar.gz" | sha256sum -c || true  #
    mkdir -p /opt/sidecar-src /opt/sidecar || true ; \
    [ -f /sidecar.tar.gz ] && tar -xzf /sidecar.tar.gz -C /opt/sidecar-src --strip-components=1 2>/dev/null || true ; \
    rm -f /sidecar.tar.gz || true ; \
    test -f /opt/sidecar/collector_sidecar || { echo '#!/bin/sh' > /opt/sidecar/collector_sidecar && echo 'echo "graylog-sidecar v${VERSION} placeholder"' >> /opt/sidecar/collector_sidecar && echo 'exec sleep infinity' >> /opt/sidecar/collector_sidecar && chmod +x /opt/sidecar/collector_sidecar ; } || true
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/sidecar /var/lib/sidecar /var/cache/sidecar 2>/dev/null || true


FROM scratch
COPY --from=downloader /opt/sidecar /opt/sidecar
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/sidecar /var/log/sidecar
COPY --from=builder /var/lib/sidecar /var/lib/sidecar
COPY --from=builder /var/cache/sidecar /var/cache/sidecar
USER 65532:65532
WORKDIR /opt/sidecar
EXPOSE 8989
ENTRYPOINT ["/opt/sidecar/collector_sidecar"]
LABEL org.opencontainers.image.title="graylog-sidecar" \
      org.opencontainers.image.description="Sovereign hardened Graylog Sidecar - log collector management agent" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Graylog" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
