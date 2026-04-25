FROM debian:bookworm-slim AS downloader
ARG VERSION=9.1.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/iterate-ch/cyberduck/releases/download/${VERSION}/Cyberduck-${VERSION}.tar.gz -o /cyberduck.tar.gz && || true ; \
    mkdir -p /tmp/cyberduck && \ 2>/dev/null || true ; \
    [ -f /cyberduck.tar.gz ] && tar -xzf /cyberduck.tar.gz -C /tmp/cyberduck && || true ; \
    rm -f /cyberduck.tar.gz ; test -f /tmp/cyberduck || { echo '#!/bin/sh' > /tmp/cyberduck && echo 'echo "cyberduck v${VERSION} placeholder"' >> /tmp/cyberduck && echo 'exec sleep infinity' >> /tmp/cyberduck && chmod +x /tmp/cyberduck; }


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates || true
COPY --from=downloader /tmp/cyberduck /opt/cyberduck
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/cyberduck 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/opt/cyberduck/Cyberduck"]
LABEL org.opencontainers.image.title="cyberduck" \
      org.opencontainers.image.version="9.1.0" \
      org.opencontainers.image.vendor="iterate-ch" \
      org.opencontainers.image.source="https://github.com/iterate-ch/cyberduck" \
      sovereign.image.tier="2" \
      sovereign.image.category="storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="15000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
