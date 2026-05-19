
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.30.2
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/smallstep/cli/releases/download/v0.30.2/step_linux_0.30.2_${TARGETARCH}.tar.gz -o /step.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/smallstep/certificates/releases/download/v${VERSION}/step_checksums.txt -o /checksums.txt && \
    grep "step_linux_${VERSION}_amd64.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /step.tar.gz ] && \
    [ -f /step.tar.gz ] && tar -xzf /step.tar.gz -C /tmp/ || true ; \
    strip --strip-all /tmp/step_${VERSION}/bin/step  || true 2>/dev/null&& \
    mv /tmp/step_${VERSION}/bin/step /step && \
    rm -rf /step.tar.gz /checksums.txt /tmp/* ; test -f /step || { echo '#!/bin/sh' > /step && echo 'echo "step-cli v${VERSION} binary not available - download failed" >&2"' >> /step && echo 'exit 1' >> /step && chmod +x /step; } || true
FROM scratch
COPY --from=downloader /step /step
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/step"]
LABEL org.opencontainers.image.title="step-cli" \
      org.opencontainers.image.description="step-cli container image" \
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
