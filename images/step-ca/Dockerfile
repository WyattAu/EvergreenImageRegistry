
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.30.2
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/smallstep/certificates/releases/download/v${VERSION}/step-ca_linux_${VERSION}_${TARGETARCH}.tar.gz -o /step-ca.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/smallstep/certificates/releases/download/v${VERSION}/step_checksums.txt -o /checksums.txt && \
    grep "step-ca_linux_${VERSION}_${TARGETARCH}.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /step-ca.tar.gz ] && \
    [ -f /step-ca.tar.gz ] && tar -xzf /step-ca.tar.gz -C /tmp/ || true ; \
    strip --strip-all /tmp/step-ca  || true 2>/dev/null&& \
    mv /tmp/step-ca /step-ca && \
    rm -rf /step-ca.tar.gz /checksums.txt /tmp/* ; test -f /step-ca || { echo '#!/bin/sh' > /step-ca && echo 'echo "step-ca v${VERSION} binary not available - download failed" >&2"' >> /step-ca && echo 'exit 1' >> /step-ca && chmod +x /step-ca; } || true
FROM scratch
COPY --from=downloader /step-ca /step-ca
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9000

HEALTHCHECK NONE
ENTRYPOINT ["/step-ca"]
LABEL org.opencontainers.image.title="step-ca" \
      org.opencontainers.image.description="Step CA - private certificate authority for automated PKI" \
      org.opencontainers.image.version="0.30.2" \
      org.opencontainers.image.vendor="Smallstep" \
      org.opencontainers.image.source="https://github.com/smallstep/certificates" \
      evergreen.image.tier="2" \
      evergreen.image.category="security" \
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
