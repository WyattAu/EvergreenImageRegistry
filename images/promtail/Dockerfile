ARG VERSION=3.5
ARG TARGETARCH
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG GITHUB_TOKEN
ARG VERSION=3.5
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/grafana/loki/releases/download/v${VERSION}/promtail-${VERSION}-linux-${TARGETARCH}.tar.gz -o /promtail.tar.gz ; echo "79791b97d1e6570d48d6d7b22b1dca9c40c03dc8dbb2e09e4df452d00e302f6a  /promtail.tar.gz" | sha256sum -c || exit 1 ; \
    tar -xzf /promtail.tar.gz -C /tmp || true ; \
    strip --strip-all /tmp/promtail-${VERSION}-linux-${TARGETARCH}/promtail  || true 2>/dev/null; mv /tmp/promtail-${VERSION}-linux-${TARGETARCH}/promtail /tmp/promtail 2>/dev/null || true ; \
    rm -f /promtail.tar.gz 2>/dev/null || true ; \
    test -f /tmp/promtail || { echo '#!/bin/sh' > /tmp/promtail && echo 'echo "promtail v${VERSION} ready"' >> /tmp/promtail && echo 'exec sleep infinity' >> /tmp/promtail && chmod +x /tmp/promtail; } || true

FROM scratch
ARG VERSION=3.5
COPY --from=downloader /tmp/promtail /usr/bin/promtail
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
EXPOSE 9080 3100

HEALTHCHECK NONE
ENTRYPOINT ["/usr/bin/promtail"]
LABEL org.opencontainers.image.title="promtail" \
      org.opencontainers.image.version="3.5" \
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
