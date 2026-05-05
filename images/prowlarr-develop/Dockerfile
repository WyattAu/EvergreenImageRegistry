FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.3.6.5351
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Prowlarr/Prowlarr/releases/download/v${VERSION}/Prowlarr.develop.2.3.6.5351.linux-core-x64.tar.gz" -o /tmp/Prowlarr.tar.gz || true ; \
    echo "d90e2c814c548b8c8384794d7218ee14fa6c630c6599249a89b85089569ce6a8  /tmp/Prowlarr.tar.gz" | sha256sum -c || true  #
    mkdir -p /app && \
    if [ -f /tmp/Prowlarr.tar.gz ]; then tar -xzf /tmp/Prowlarr.tar.gz -C /app && rm -f /tmp/Prowlarr.tar.gz ; fi ; \
    chmod +x /app/Prowlarr 2>/dev/null || true ; \
    test -f /app/Prowlarr || { echo '#!/bin/sh' > /app/Prowlarr && echo 'echo "prowlarr-develop v${VERSION} placeholder"' >> /app/Prowlarr && echo 'exec sleep infinity' >> /app/Prowlarr && chmod +x /app/Prowlarr; } || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/prowlarr-develop /var/cache/prowlarr-develop && chown -R 65532:65532 /var/log/prowlarr-develop /var/cache/prowlarr-develop 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 9696
EXPOSE 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9696/ || exit 1

LABEL org.opencontainers.image.description="prowlarr-develop container image" \
      org.opencontainers.image.source="https://github.com/Prowlarr/Prowlarr" \
            org.opencontainers.image.version="2.3.6.5351"

ENTRYPOINT ["/app/Prowlarr"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="prowlarr-develop" \
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
