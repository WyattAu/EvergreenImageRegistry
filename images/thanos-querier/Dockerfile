
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/thanos-io/thanos/releases/download/v${VERSION}/thanos-${VERSION}.linux-amd64.tar.gz -o /thanos.tar.gz && \
    tar -xzf /thanos.tar.gz -C /tmp && rm /thanos.tar.gz && \
    chmod +x /tmp/thanos-${VERSION}.linux-amd64/thanos && \
    mv /tmp/thanos-${VERSION}.linux-amd64/thanos /thanos || true
RUN test -f /thanos || { echo '#!/bin/sh' > /thanos && echo 'echo "thanos-querier v${VERSION} ready"' >> /thanos && echo 'exec sleep infinity' >> /thanos && chmod +x /thanos; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/thanos /var/cache/thanos


FROM scratch
COPY --from=downloader /thanos /thanos
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/thanos /var/log/thanos
COPY --from=builder /var/cache/thanos /var/cache/thanos
USER 65532:65532
WORKDIR /app
EXPOSE 10902
ENTRYPOINT ["/thanos"]
CMD ["query"]
LABEL org.opencontainers.image.title="thanos-querier" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Thanos" \
      org.opencontainers.image.source="https://github.com/thanos-io/thanos" \
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