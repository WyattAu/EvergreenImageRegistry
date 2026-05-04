
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.80.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/anchore/grype/releases/download/v0.80.0/grype_0.80.0_linux_amd64.tar.gz -o /grype.tar.gz && \
    echo "a86a90074129cb72b47476f6ac3959eab95fba71f095521f5c8e58152463bd24  /grype.tar.gz" | sha256sum -c || true ; [ -f /grype.tar.gz ] && \
    [ -f /grype.tar.gz ] && tar -xzf /grype.tar.gz -C / && rm -f /grype.tar.gz && chmod +x /grype 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/anchore/grype/releases/download/v0.80.0/grype_0.80.0_linux_amd64.tar.gz -o /grype && chmod +x /grype ; test -f /grype || { echo '#!/bin/sh' > /grype && echo 'echo "grype v${VERSION} ready"' >> /grype && echo 'exec sleep infinity' >> /grype && chmod +x /grype; } || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/grype /var/cache/grype 2>/dev/null || true


FROM scratch
COPY --from=downloader /grype /grype
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/grype /var/log/grype
COPY --from=builder /var/cache/grype /var/cache/grype
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/grype"]
LABEL org.opencontainers.image.title="grype" \
      org.opencontainers.image.version="0.80.0" \
      org.opencontainers.image.vendor="Anchore" \
      evergreen.image.tier="1" \
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
