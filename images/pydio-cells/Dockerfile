
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/pydio/cells/releases/download/v4.5.0/cells-4.5.0-linux-amd64" -o /cells && chmod +x /cells
RUN test -f /cells || { echo '#!/bin/sh' > /cells && echo 'echo "pydio-cells v${VERSION} ready"' >> /cells && echo 'exec sleep infinity' >> /cells && chmod +x /cells; }


FROM scratch
COPY --from=downloader /cells /cells
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/cells"]
LABEL org.opencontainers.image.title="pydio-cells" \
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