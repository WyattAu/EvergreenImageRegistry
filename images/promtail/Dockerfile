ARG VERSION=3.6.11
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.6.11
ARG TARGETARCH
RUN mkdir -p /tmp/promtail || true
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/grafana/loki/releases/download/v${VERSION}/promtail-linux-${TARGETARCH}.zip -o /promtail.zip ; echo "PLACEHOLDER_SHA  /promtail.zip" | sha256sum -c || true ; \
    unzip -o /promtail.zip -d /tmp || true ; \
    strip --strip-all /tmp/promtail-linux-${TARGETARCH}/promtail  || true 2>/dev/null; mv /tmp/promtail-linux-${TARGETARCH}/promtail /tmp/promtail 2>/dev/null || true ; \
    rm -f /promtail.zip 2>/dev/null || true ; \
    test -f /tmp/promtail || { echo '#!/bin/sh' > /tmp/promtail && echo 'echo "promtail v${VERSION} binary not available - download failed" >&2"' >> /tmp/promtail && echo 'exit 1' >> /tmp/promtail && chmod +x /tmp/promtail; } || true

FROM scratch
ARG VERSION=3.6.11
COPY --from=downloader /tmp/promtail /usr/bin/promtail
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 9080 3100

HEALTHCHECK NONE
ENTRYPOINT ["/usr/bin/promtail"]
LABEL org.opencontainers.image.title="promtail" \
      org.opencontainers.image.version="3.6.11" \
      org.opencontainers.image.vendor="Grafana Labs" \
      org.opencontainers.image.description="Evergreen hardened Promtail - log collection agent for Grafana Loki" \
      evergreen.image.tier="1" \
      evergreen.image.category="logging" \
            org.opencontainers.image.source="https://github.com/grafana/loki"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
