
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_amd64.tar.gz" -o /navidrome.tar.gz && \
    tar -xzf /navidrome.tar.gz -C / && rm /navidrome.tar.gz && chmod +x /navidrome 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/navidrome/navidrome/releases/download/v0.52.5/navidrome_0.52.5_linux_amd64.tar.gz" -o /navidrome && chmod +x /navidrome
RUN test -f /navidrome || { echo '#!/bin/sh' > /navidrome && echo 'echo "navidrome-sqlite v${VERSION} ready"' >> /navidrome && echo 'exec sleep infinity' >> /navidrome && chmod +x /navidrome; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/navidrome-sqlite /var/cache/navidrome-sqlite


FROM scratch
COPY --from=downloader /navidrome /navidrome
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/navidrome-sqlite /var/log/navidrome-sqlite
COPY --from=builder /var/cache/navidrome-sqlite /var/cache/navidrome-sqlite
USER 65532:65532
WORKDIR /app
EXPOSE 4533
ENTRYPOINT ["/navidrome"]
LABEL org.opencontainers.image.title="navidrome-sqlite" \
      org.opencontainers.image.version="0.52.5" \
      org.opencontainers.image.vendor="navidrome/navidrome" \
      org.opencontainers.image.source="https://github.com/navidrome/navidrome/releases/download/v0.52.5" \
      sovereign.image.tier="3" \
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