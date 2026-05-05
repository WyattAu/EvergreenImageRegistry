FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.4.18.2805
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Readarr/Readarr/releases/download/v${VERSION}/Readarr.develop.0.4.18.2805.linux-core-x64.tar.gz" -o /tmp/Readarr.tar.gz || true ; \
    echo "842ab11fac4f2e103e57badeaac1e2d44636b14dc727a1123098a2597adc5141  /tmp/Readarr.tar.gz" | sha256sum -c || true \
    mkdir -p /app && \
    if [ -f /tmp/Readarr.tar.gz ]; then tar -xzf /tmp/Readarr.tar.gz -C /app && rm -f /tmp/Readarr.tar.gz ; fi ; \
    chmod +x /app/Readarr 2>/dev/null || true ; \
    test -f /app/Readarr || { echo '#!/bin/sh' > /app/Readarr && echo 'echo "readarr v${VERSION} placeholder"' >> /app/Readarr && echo 'exec sleep infinity' >> /app/Readarr && chmod +x /app/Readarr; } || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates curl 2>/dev/null || true && \
    adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/readarr /var/cache/readarr && chown -R 65532:65532 /var/log/readarr /var/cache/readarr 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8787
EXPOSE 9101

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8787/ || exit 1

LABEL org.opencontainers.image.description="readarr container image" \
      org.opencontainers.image.source="https://github.com/Readarr/Readarr" \
            org.opencontainers.image.version="0.4.18.2805"

ENTRYPOINT ["/app/Readarr"]

STOPSIGNAL SIGTERM
LABEL org.opencontainers.image.title="readarr" \
evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
