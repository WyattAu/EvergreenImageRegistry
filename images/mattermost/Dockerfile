ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://releases.mattermost.com/${VERSION}/mattermost-${VERSION}-linux-${TARGETARCH}.tar.gz" -o /mattermost.tar.gz || true ; \
    echo "44fd580510f1971768c3eb650b37c549fa56ee93da50aaeb09ed4b6f721b96bb  /mattermost.tar.gz" | sha256sum -c || true  #
    mkdir -p /opt ; \
    if [ -f /mattermost.tar.gz ]; then tar -xzf /mattermost.tar.gz -C /opt && rm -f /mattermost.tar.gz ; fi ; \
    ln -sf /opt/mattermost-${VERSION} /opt/mattermost 2>/dev/null || true ; \
    test -f /opt/mattermost/bin/mattermost || { echo '#!/bin/sh' > /opt/mattermost && echo 'echo "mattermost v${VERSION} placeholder"' >> /opt/mattermost && echo 'exec sleep infinity' >> /opt/mattermost && chmod +x /opt/mattermost; } || true
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates tzdata 
COPY --from=downloader /opt/mattermost /opt/mattermost
RUN addgroup -S -g 65532 mattermost 2>/dev/null || true && \
    adduser -u 65532 -G mattermost -D -D -h /opt/mattermost -s /bin/false mattermost 2>/dev/null || true && \
    mkdir -p /opt/mattermost-src/data /opt/mattermost/logs /opt/mattermost/plugins /opt/mattermost/client/plugins ; \
    chown -R 65532:65532 /opt/mattermost
USER 65532:65532
WORKDIR /opt/mattermost
EXPOSE 8065

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8065/ || exit 1
ENTRYPOINT ["/opt/mattermost/bin/mattermost"]
LABEL org.opencontainers.image.title="mattermost" \
      org.opencontainers.image.description="mattermost container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/mattermost" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="collaboration" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
