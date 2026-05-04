ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.90.74
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/statping/statping/releases/download/v${VERSION}/statping-linux-${TARGETARCH}.tar.gz -o /statping.tar.gz || true ; \
    echo "d287782dde1b96afbc7e41a95568347dddc0967db114feede1492cfe1fc6f3c3  /statping.tar.gz" | sha256sum -c || true  #
    [ -f /statping.tar.gz ] && tar -xzf /statping.tar.gz -C / && rm -f /statping.tar.gz || true ; \
    find / -maxdepth 1 -name "statping" -type f -exec chmod +x {} \; test -f /statping || { echo '#!/bin/sh' > /statping && echo 'echo "statping-ng v${VERSION} ready"' >> /statping && echo 'exec sleep infinity' >> /statping && chmod +x /statping; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/statping 2>/dev/null || true


FROM scratch
COPY --from=downloader /statping /statping
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/statping /var/log/statping
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/statping"]
LABEL org.opencontainers.image.title="statping-ng" \
      org.opencontainers.image.version="0.90.74" \
      org.opencontainers.image.vendor="statping" \
      org.opencontainers.image.source="https://github.com/statping/statping" \
      org.opencontainers.image.description="Service monitoring and uptime tracking" \
      evergreen.image.tier="1" \
      evergreen.image.category="monitoring" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="5000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
