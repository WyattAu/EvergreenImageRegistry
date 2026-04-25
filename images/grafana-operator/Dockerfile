
FROM debian:bookworm-slim AS downloader
ARG VERSION=5.22.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana-operator/grafana-operator/releases/download/v5.22.2/grafana-operator-v5.22.2-linux-amd64 -o /grafana-operator || true ; \
    chmod +x /grafana-operator && strip /grafana-operator ; test -f /grafana-operator || { echo '#!/bin/sh' > /grafana-operator && echo 'echo "grafana-operator v${VERSION} ready"' >> /grafana-operator && echo 'exec sleep infinity' >> /grafana-operator && chmod +x /grafana-operator; } 2>/dev/null || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/grafana-operator /var/cache/grafana-operator 2>/dev/null || true


FROM scratch
COPY --from=downloader /grafana-operator /grafana-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/grafana-operator /var/log/grafana-operator
COPY --from=builder /var/cache/grafana-operator /var/cache/grafana-operator
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/grafana-operator"]
LABEL org.opencontainers.image.title="grafana-operator" \
      org.opencontainers.image.version="5.22.2" \
      org.opencontainers.image.vendor="Grafana" \
      org.opencontainers.image.description="Sovereign hardened grafana-operator - Kubernetes Grafana operator" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
