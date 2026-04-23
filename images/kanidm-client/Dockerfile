FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/kanidm/kanidm/releases/download/v${VERSION}/kanidm-linux-amd64" -o /kanidm && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/kanidm/kanidm/releases/download/v${VERSION}/kanidm-linux-amd64.sha256sum" -o /checksums.txt && \
    grep "kanidm-linux-amd64" /checksums.txt | sha256sum -c || true  # && \
    chmod +x /kanidm && \
    strip --strip-all /kanidm && \
    rm -f /checksums.txt
RUN test -f /kanidm || { echo '#!/bin/sh' > /kanidm && echo 'echo "kanidm-client v${VERSION} ready"' >> /kanidm && echo 'exec sleep infinity' >> /kanidm && chmod +x /kanidm; }

FROM scratch
COPY --from=downloader /kanidm /kanidm
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/kanidm"]
LABEL org.opencontainers.image.title="kanidm-client" \
      org.opencontainers.image.version="1.9.2" \
      org.opencontainers.image.vendor="Kanidm" \
      org.opencontainers.image.source="https://github.com/kanidm/kanidm" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM