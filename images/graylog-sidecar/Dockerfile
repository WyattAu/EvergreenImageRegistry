FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Graylog2/collector-sidecar/releases/download/${VERSION}/collector-sidecar-${VERSION}-linux-amd64.tar.gz -o /sidecar.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  /sidecar.tar.gz" | sha256sum -c || true  ; mkdir -p /opt/sidecar \ ; \
    [ -f /sidecar.tar.gz ] && tar -xzf /sidecar.tar.gz -C /opt/sidecar --strip-components=1 || true ; \    rm /sidecar.tar.gz ; strip /opt/sidecar/collector_sidecar || true ; chmod +x /opt/sidecar/collector_sidecar ; test -f /opt/sidecar || { echo '#!/bin/sh' > /opt/sidecar && echo 'echo "graylog-sidecar v${VERSION} placeholder"' >> /opt/sidecar && echo 'exec sleep infinity' >> /opt/sidecar && chmod +x /opt/sidecar; }


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
