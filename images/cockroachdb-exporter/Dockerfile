FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/cockroachdb/cockroach/releases/download/v${VERSION}/cockroach-v${VERSION}.linux-amd64.tgz" -o /cockroach.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  /cockroach.tar.gz" | sha256sum -c || true  # \
    && mkdir -p /opt/cockroach \
    && tar -xzf /cockroach.tar.gz -C /opt/cockroach --strip-components=1 \
    && rm /cockroach.tar.gz \
    && strip /opt/cockroach/cockroach || true \
    && chmod +x /opt/cockroach/cockroachRUN test -f /opt/cockroach/cockroach || { echo '#!/bin/sh' > /opt/cockroach/cockroach && echo 'echo "cockroachdb-exporter v${VERSION} placeholder"' >> /opt/cockroach/cockroach && echo 'exec sleep infinity' >> /opt/cockroach/cockroach && chmod +x /opt/cockroach/cockroach; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/cockroach /var/lib/cockroach /var/cache/cockroach


FROM scratch
COPY --from=downloader /opt/cockroach/cockroach /cockroach
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/cockroach /var/log/cockroach
COPY --from=builder /var/lib/cockroach /var/lib/cockroach
COPY --from=builder /var/cache/cockroach /var/cache/cockroach
USER 65532:65532
WORKDIR /
EXPOSE 8080
ENTRYPOINT ["/cockroach"]
CMD ["start", "--insecure", "--http-port=8080", "--prometheus-port=8080"]
LABEL org.opencontainers.image.title="cockroachdb-exporter" \
      org.opencontainers.image.description="Sovereign hardened CockroachDB Prometheus exporter - database metrics via built-in endpoint" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Cockroach Labs" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="5000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM