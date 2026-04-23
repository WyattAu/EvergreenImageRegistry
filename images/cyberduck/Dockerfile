
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/iterate-ch/cyberduck/releases/download/${VERSION}/Cyberduck-${VERSION}.tar.gz" -o /cyberduck.tar.gz && \
    mkdir -p /tmp/cyberduck && \
    tar -xzf /cyberduck.tar.gz -C /tmp/cyberduck && \
    rm -f /cyberduck.tar.gz




FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=downloader /tmp/cyberduck /opt/cyberduck
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/cyberduck
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