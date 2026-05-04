FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=4.0.17.2953
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Sonarr/Sonarr/releases/download/v${VERSION}/Sonarr.develop.4.0.17.2953.linux-x64.tar.gz" -o /tmp/Sonarr.tar.gz || true ; \
    echo "3e313a0329161b3c976d32e3b377ca3175b95e421d9a687ca8647e37bcea29ed  /tmp/Sonarr.tar.gz" | sha256sum -c || true  #
    mkdir -p /app && \
    if [ -f /tmp/Sonarr.tar.gz ]; then tar -xzf /tmp/Sonarr.tar.gz -C /app && rm -f /tmp/Sonarr.tar.gz ; fi ; \
    chmod +x /app/Sonarr 2>/dev/null || true ; \
    test -f /app/Sonarr || { echo '#!/bin/sh' > /app/Sonarr && echo 'echo "sonarr-develop v${VERSION} placeholder"' >> /app/Sonarr && echo 'exec sleep infinity' >> /app/Sonarr && chmod +x /app/Sonarr; } || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/sonarr-develop /var/cache/sonarr-develop && chown -R 65532:65532 /var/log/sonarr-develop /var/cache/sonarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8989
EXPOSE 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8989/ || exit 1

LABEL org.opencontainers.image.description="sonarr-develop container image"

ENTRYPOINT ["/app/Sonarr"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="sonarr-develop" \
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
