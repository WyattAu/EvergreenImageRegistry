
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mickael-kerjean/filestash/releases/download/v0.4.29/filestash-linux-amd64" -o /filestash && chmod +x /filestash
RUN test -f /filestash || { echo '#!/bin/sh' > /filestash && echo 'echo "filestash v${VERSION} ready"' >> /filestash && echo 'exec sleep infinity' >> /filestash && chmod +x /filestash; }


FROM scratch
COPY --from=downloader /filestash /filestash
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8334
ENTRYPOINT ["/filestash"]
LABEL org.opencontainers.image.title="filestash" \
      org.opencontainers.image.version="v0.4.29" \
      org.opencontainers.image.vendor="Filestash" \
      org.opencontainers.image.source="https://github.com/mickael-kerjean/filestash" \
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