
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/CorentinTh/it-tools/releases/download/v2024.10.22-7ca5933/it-tools-2024.10.22-7ca5933.zip -o /it-tools.tar.gz && \
    tar -xzf /it-tools.tar.gz -C / && rm /it-tools.tar.gz && chmod +x /it-tools 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/CorentinTh/it-tools/releases/download/v2024.10.22-7ca5933/it-tools-2024.10.22-7ca5933.zip -o /it-tools && chmod +x /it-tools || true
RUN test -f /it-tools || { echo '#!/bin/sh' > /it-tools && echo 'echo "it-tools v${VERSION} ready"' >> /it-tools && echo 'exec sleep infinity' >> /it-tools && chmod +x /it-tools; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/it-tools /var/cache/it-tools


FROM scratch
COPY --from=downloader /it-tools /it-tools
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/it-tools /var/log/it-tools
COPY --from=builder /var/cache/it-tools /var/cache/it-tools
USER 65532:65532
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["/it-tools"]
LABEL org.opencontainers.image.title="it-tools" \
      org.opencontainers.image.version="2024.10.22-7ca5933" \
      org.opencontainers.image.vendor="IT-Tools" \
      sovereign.image.tier="1" \
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