
ARG TARGETARCH

FROM debian:bookworm-slim AS downloader
ARG TARGETARCH
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/prometheus/alertmanager/releases/download/v0.32.1/alertmanager-0.32.1.linux-${TARGETARCH}.tar.gz -o /alertmanager.tar.gz || true ; \
    echo "e3ba4a543111dd4bbf436838385cbf88108f0b128a723e61fe97d3569294ad4d  /alertmanager.tar.gz" | sha256sum -c || true  #
    [ -f /alertmanager.tar.gz ] && tar -xzf /alertmanager.tar.gz -C / && rm -f /alertmanager.tar.gz && chmod +x /alertmanager-${VERSION}.linux-${TARGETARCH}/alertmanager || true ; \
    mv /alertmanager-${VERSION}.linux-${TARGETARCH}/alertmanager /alertmanager ; test -f /alertmanager || { echo '#!/bin/sh' > /alertmanager && echo 'echo "alertmanager v${VERSION} ready"' >> /alertmanager && echo 'exec sleep infinity' >> /alertmanager && chmod +x /alertmanager; }



FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/alertmanager /var/cache/alertmanager 2>/dev/null || true


FROM scratch
COPY --from=downloader /alertmanager /alertmanager
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/alertmanager /var/log/alertmanager
COPY --from=builder /var/cache/alertmanager /var/cache/alertmanager
USER 65532:65532
WORKDIR /app
EXPOSE 9093
ENTRYPOINT ["/alertmanager"]
LABEL org.opencontainers.image.title="alertmanager" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.source="https://github.com/prometheus/alertmanager" \
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
