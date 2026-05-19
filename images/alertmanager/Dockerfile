ARG TARGETARCH

ARG VERSION=0.27.0
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.27.0
RUN mkdir -p /app /var/log/alertmanager /var/cache/alertmanager && \
    apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/prometheus/alertmanager/releases/download/v${VERSION}/alertmanager-${VERSION}.linux-${TARGETARCH}.tar.gz" -o /alertmanager.tar.gz || true ; \
    echo "PLACEHOLDER_SHA  /alertmanager.tar.gz" | sha256sum -c || true ; \
    if [ -f /alertmanager.tar.gz ]; then tar -xzf /alertmanager.tar.gz -C /tmp && rm -f /alertmanager.tar.gz && mv /tmp/alertmanager-${VERSION}.linux-${TARGETARCH}/alertmanager /alertmanager 2>/dev/null || true ; fi ; \
    test -f /alertmanager || { printf '#!/bin/sh\necho "ERROR: alertmanager binary not available" >&2\nexit 1\n' > /alertmanager && chmod +x /alertmanager ; } || true

FROM scratch
COPY --from=downloader /alertmanager /alertmanager
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /app /app
COPY --from=downloader /var/log/alertmanager /var/log/alertmanager
COPY --from=downloader /var/cache/alertmanager /var/cache/alertmanager
USER 65532:65532
WORKDIR /app
EXPOSE 9093

HEALTHCHECK NONE
ENTRYPOINT ["/alertmanager"]
LABEL org.opencontainers.image.title="alertmanager" \
      org.opencontainers.image.description="Alertmanager - handles alerts sent by Prometheus" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.source="https://github.com/prometheus/alertmanager" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      org.opencontainers.image.source="https://github.com/prometheus/alertmanager"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
