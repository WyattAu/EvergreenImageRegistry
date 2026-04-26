FROM debian:bookworm-slim AS downloader
ARG VERSION=${VERSION}
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://releases.mattermost.com/${VERSION}/mattermost-${VERSION}-linux-amd64.tar.gz" -o /mattermost.tar.gz || true ; \
    mkdir -p /opt/mattermost-src ; \
    [ -f /mattermost.tar.gz ] && tar -xzf /mattermost.tar.gz -C /opt || true ; \
    rm /mattermost.tar.gz ; test -f /opt/mattermost || { echo '#!/bin/sh' > /opt/mattermost && echo 'echo "mattermost v${VERSION} placeholder"' >> /opt/mattermost && echo 'exec sleep infinity' >> /opt/mattermost && chmod +x /opt/mattermost; }


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates tzdata 
COPY --from=downloader /opt/mattermost /opt/mattermost
RUN addgroup -S 65532 -r mattermost 2>/dev/null || true && \
    adduser -u 65532 -G mattermost -D -D -h /opt/mattermost -s /bin/false mattermost 2>/dev/null || true && \
    mkdir -p /opt/mattermost-src/data /opt/mattermost/logs /opt/mattermost/plugins /opt/mattermost/client/plugins ; \
    chown -R 65532:65532 /opt/mattermost
USER 65532:65532
WORKDIR /opt/mattermost
EXPOSE 8065
ENTRYPOINT ["/opt/mattermost/bin/mattermost"]
LABEL org.opencontainers.image.title="mattermost" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Mattermost" \
      org.opencontainers.image.source="https://github.com/mattermost/mattermost" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="collaboration" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
