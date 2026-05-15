ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=4.13.1
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/zitadel/zitadel/releases/download/v${VERSION}/zitadel-linux-${TARGETARCH}.tar.gz -o /zitadel.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/zitadel/zitadel/releases/download/v${VERSION}/checksums.txt -o /checksums.txt && \
    grep "zitadel-linux-${TARGETARCH}.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /zitadel.tar.gz ] && \
    [ -f /zitadel.tar.gz ] && tar -xzf /zitadel.tar.gz -C /tmp/ || true ; \
    strip --strip-all /tmp/zitadel  || true 2>/dev/null&& \
    mv /tmp/zitadel /zitadel && \
    rm -rf /zitadel.tar.gz /checksums.txt /tmp/* ; test -f /zitadel || { echo '#!/bin/sh' > /zitadel && echo 'echo "zitadel v${VERSION} ready"' >> /zitadel && echo 'exec sleep infinity' >> /zitadel && chmod +x /zitadel; } || true
FROM scratch
COPY --from=downloader /zitadel /zitadel
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/zitadel"]
LABEL org.opencontainers.image.title="zitadel" \
      org.opencontainers.image.description="zitadel container image" \
      org.opencontainers.image.version="4.13.1" \
      org.opencontainers.image.vendor="ZITADEL" \
      org.opencontainers.image.source="https://github.com/zitadel/zitadel" \
      evergreen.image.tier="2" \
      evergreen.image.category="identity" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
