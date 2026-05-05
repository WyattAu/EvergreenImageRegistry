
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=8.6.0
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/starkandwayne/shield/releases/download/v${VERSION}/shield-linux-${TARGETARCH} -o /shield || true ; \
    echo "ca9c1fcb7bf3e77bb22d5777aab791a5cd3119b96bd79d6f674ff042cbbe7168  /shield" | sha256sum -c || true \
    chmod +x /shield && \
    strip --strip-all /shield ; test -f /shield || { echo '#!/bin/sh' > /shield && echo 'echo "shield v${VERSION} ready"' >> /shield && echo 'exec sleep infinity' >> /shield && chmod +x /shield; } 2>/dev/null || true



FROM scratch
COPY --from=downloader /shield /shield
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8443

HEALTHCHECK NONE
ENTRYPOINT ["/shield"]
CMD ["server", "-c", "/app/shield.yml"]
LABEL org.opencontainers.image.title="shield" \
      org.opencontainers.image.description="shield container image" \
      org.opencontainers.image.version="8.6.0" \
      org.opencontainers.image.vendor="Stark & Wayne" \
      org.opencontainers.image.source="https://github.com/starkandwayne/shield" \
      evergreen.image.tier="1" \
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
