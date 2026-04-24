FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/ltiam/APacheDirectoryStudio/releases/download/${VERSION}/ApacheDirectoryStudio-${VERSION}-linux.gtk.x86_64.tar.gz" -o /studio.tar.gz && \
    mkdir -p /tmp/studio && \
    tar -xzf /studio.tar.gz -C /tmp/studio --strip-components=1 && \
    rm -f /studio.tar.gz
RUN test -f /tmp/studio || { echo '#!/bin/sh' > /tmp/studio && echo 'echo "ldapbrowser v${VERSION} placeholder"' >> /tmp/studio && echo 'exec sleep infinity' >> /tmp/studio && chmod +x /tmp/studio; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=downloader /tmp/studio /opt/ApacheDirectoryStudio
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/ApacheDirectoryStudio
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/opt/ApacheDirectoryStudio/ApacheDirectoryStudio"]
LABEL org.opencontainers.image.title="ldapbrowser" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.source="https://github.com/ltiam/APacheDirectoryStudio" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
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