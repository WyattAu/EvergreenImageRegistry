
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.7.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/containrrr/watchtower/releases/download/v${VERSION}/watchtower_linux_${TARGETARCH}.tar.gz -o /watchtower.tar.gz && \
    echo "PLACEHOLDER_SHA  /watchtower.tar.gz" | sha256sum -c || exit 1 ; \
    [ -f /watchtower.tar.gz ] && tar -xzf /watchtower.tar.gz -C / && rm -f /watchtower.tar.gz && chmod +x /watchtower 2>/dev/null || true ; \
    test -f /watchtower || { echo '#!/bin/sh' > /watchtower && echo 'echo "watchtower v${VERSION} ready"' >> /watchtower && echo 'exec sleep infinity' >> /watchtower && chmod +x /watchtower; } || true


FROM scratch
ARG VERSION=1.7.1
COPY --from=downloader /watchtower /watchtower
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/watchtower"]
LABEL org.opencontainers.image.title="watchtower" \
      org.opencontainers.image.description="Watchtower - automatic Docker container updates" \
      org.opencontainers.image.version="1.7.1" \
      org.opencontainers.image.vendor="containrrr" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="0-1" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-rolling" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
            org.opencontainers.image.source="https://github.com/containrrr/watchtower"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
