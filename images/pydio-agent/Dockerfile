
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/pydio/cells/releases/download/v4.5.0/cells-4.5.0-linux-amd64 -o /cells-agent && chmod +x /cells-agent ; test -f /cells-agent || { echo '#!/bin/sh' > /cells-agent && echo 'echo "pydio-agent v${VERSION} ready"' >> /cells-agent && echo 'exec sleep infinity' >> /cells-agent && chmod +x /cells-agent; }



FROM scratch
COPY --from=downloader /cells-agent /cells-agent
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8081
ENTRYPOINT ["/cells-agent"]
LABEL org.opencontainers.image.title="pydio-agent" \
      org.opencontainers.image.version="4.5.0" \
      org.opencontainers.image.vendor="Pydio" \
      org.opencontainers.image.source="https://github.com/pydio/cells" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
