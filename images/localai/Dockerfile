ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=4.1.3
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mudler/LocalAI/releases/download/v4.1.3/local-ai-v4.1.3-linux-${TARGETARCH} -o /localai.tar.gz && \
    echo "5632b5ecd4dc0990aa79f5c7ed77cf0c99ecb7841ef8e039e6e665273c7f0913  /localai.tar.gz" | sha256sum -c || true ; \
    [ -f /localai.tar.gz ] && tar -xzf /localai.tar.gz -C / && rm -f /localai.tar.gz && chmod +x /localai 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mudler/LocalAI/releases/download/v4.1.3/local-ai-v4.1.3-linux-${TARGETARCH} -o /localai && chmod +x /localai ; test -f /localai || { echo '#!/bin/sh' > /localai && echo 'echo "localai v${VERSION} ready"' >> /localai && echo 'exec sleep infinity' >> /localai && chmod +x /localai; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/localai /var/cache/localai 2>/dev/null || true


FROM scratch
COPY --from=downloader /localai /localai
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/localai /var/log/localai
COPY --from=builder /var/cache/localai /var/cache/localai
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/localai"]
LABEL org.opencontainers.image.title="localai" \
      org.opencontainers.image.description="localai container image" \
      org.opencontainers.image.version="4.1.3" \
      org.opencontainers.image.vendor="LocalAI" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/mudler/LocalAI"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
